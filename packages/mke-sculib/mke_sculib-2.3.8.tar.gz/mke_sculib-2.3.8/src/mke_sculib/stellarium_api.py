import requests
import numpy as np
import datetime
import asyncio
import time
import threading
from astropy.time import Time

class stellarium_api(threading.Thread):
    
    def __init__(self, scu_api, address = 'http://localhost:8090',
                    lat = -30.7249,
                    lon = 21.45714,
                    altitude = 1086,
                    name = 'meerkat_site',
                    country = 'South Africa',
                    use_async=True, 
                    verb=True, 
                    use_socket=False):
        """interfacing class for a stellarium program with remote control enabled

        Args:
            scu_api (mke_client.scu.scu): the api accessor to use for a mke scu
            address (str, optional): the uri address for the stellarium program. Defaults to 'http://localhost:8090'.
            lat (float, optional): the latitude location to set. Defaults to -30.7249.
            lon (float, optional): the longitude location to set. Defaults to 21.45714.
            altitude (int, optional): the altitude to set (in meter). Defaults to 1086.
            name (str, optional): the name to give the location. Defaults to 'meerkat_site'.
            country (str, optional): name for the country. Defaults to 'South Africa'.
            use_async (bool, optional): whether or not to use async. Defaults to True.
            verb (bool, optional): give info in stdout. Defaults to True.
            use_socket (bool, optional): whether or not to use websockets or http. Defaults to False.
        """

        threading.Thread.__init__(self)

        self.address = address
        self.lat = lat
        self.lon = lon
        self.altitude = altitude
        self.loc_name = name
        self.country = country
        
        self.scu_api = scu_api
        self.verb = verb
        self.use_async = use_async
        self.use_socket = use_socket

        self._event_stop = threading.Event()

        self._t_last = datetime.datetime.utcnow()
        self._data = {}
        self.info = ''

    @property
    def is_stopped(self):
        return self._event_stop.is_set()
    
    def stop(self):
        self._event_stop.set()

    def ping(self):
        """ping the stellarium api

        Returns:
            dict: empty if not available otherwise the current status
        """
        r = requests.get(self.address + '/api/main/status')
        if r.status_code != 200:
            return {}
        else:
            return r.json()

    def get_status(self):
        """get current status in stellarium

        Returns:
            dict: status of the program as dict
        """
        r = requests.get(self.address + '/api/main/status')
        r.raise_for_status()
        return r.json()
    
    def set_loc(self):
        """set the location as given during construction to the stellarium api
        """


        r = requests.post(self.address + '/api/location/setlocationfields', params = {                      
            'latitude': self.lat,
            'longitude': self.lon,
            'altitude': self.altitude,
            'name': self.loc_name,
            'country': self.country
        })
        r.raise_for_status()


    def set_boresight(self, az, el):
        """set the boresight location

        Args:
            az (float): azimuth position in DEGREE
            el (float): elevation position in DEGREE
        """
        az = (180 - az) % 360 # stellarium az definition != mke az definition MKE 0 = North +90 = East
        r = requests.post(self.address + '/api/main/view', params={'az': np.deg2rad(az), 'alt': np.deg2rad(el)})
        r.raise_for_status()


    def move_boresight(self, x, y):
        """joystick like move the boresight (setting an angular speed)

        Args:
            x (float): number -1...+1 with neg = move left and pos = move right
            y (float): number -1...+1 with neg = move down pos = move up
        """
        r = requests.post(self.address + '/api/main/move', params={'x': np.clip(x, -1, 1), 'y': np.clip(y, -1, 1)})
        r.raise_for_status()


    def set_time(self, time):
        """set the internal time in stellarium

        Args:
            time (astropy.time.Time): the internal telescope time
        """
        r = requests.post(self.address + '/api/main/time', params={'time': time.jd})
        r.raise_for_status()

    def _run_init(self, scu_api, verb):
        if verb: 
            print('initializing contact with app...')
            
        status = self.ping()
        if not status:
            raise ConnectionError('Could not connect to the stellarium program. Make sure the program is running and has remote control plugin enabled')
        if verb:
            print('--> OK')
            print('current status ins stellarium:')
            print(status)
            print('Setting config...')
        self.set_time(scu_api.t_internal)
        self.set_loc()
        if verb:
            print('--> OK')
            print('current status ins stellarium:')
            print(self.get_status())
            print('starting periodic update...')
            print('')
            print(' TIME (UTC)          | AZIMUTH (deg) | ELEVATION (deg) | FPS')

    
    
    def run(self):
        """runs a continious feedthrough interface to 
            translate between a Meerkat Extension Dish 
            and Stellarium.
        """
        self.loc_name += '-' + self.scu_api.address
        self._run_init(self.scu_api, self.verb)

        if self.use_async:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._loop_run_async(self.scu_api, verb=self.verb, use_socket=self.use_socket))
            loop.close()
        else:
            self._loop_run_sync(self.scu_api, self.verb)
    
    async def run_async(self):
        """runs a continious feedthrough interface to 
            translate between a Meerkat Extension Dish 
            and Stellarium.
        """
        self.loc_name += '-' + self.scu_api.address
        self._run_init(self.scu_api, self.verb)

        assert self.use_async, 'must be using async'
        await self._loop_run_async(self.scu_api, verb=self.verb, use_socket=self.use_socket)

    def _tick_info(self, t, az, el):        
        dt = abs((t - self._t_last).total_seconds())
        fps = 0. if dt <= 0 else 1/dt
        info = ' {} | AZ={: 10.4f} | EL={: 10.4f}   | FPS={: 4.2f}'.format(t.isoformat().split('.')[0], az % 360, el, fps)
        self.info = f'Synched with: {self.scu_api.address}\n{info}' 
        self._info = info
        self._t_last = t

    def _loop_run_sync(self, scu_api, verb=True, use_socket=False):


        if use_socket:
            _, fields = next(gen)
        channels = ['acu.azimuth.p_act', 'acu.elevation.p_act']
        gen = scu_api.sock_listen_forever(channels)

        while 1:
            if self.is_stopped:
                return

            if use_socket:
                _, fields = next(gen)
                az, el = fields.values()

            else:
                az, el = scu_api.azel
            
            if self.is_stopped:
                return
            
            self._tick_info(datetime.datetime.utcnow(), az, el)
            self.set_boresight(az, el)
            if verb:
                print(self._info, end='\r')
            self._data = {'az': np.deg2rad(az), 'alt': np.deg2rad(el)}

    async def _loop_run_async(self, scu_api, verb=True, use_socket=False):

        import aiohttp, json

        channels = ['acu.azimuth.p_act', 'acu.elevation.p_act']
        url = self.address + '/api/main/view'
        
        if use_socket:
            gen = scu_api.sock_listen_forever_async(channels)


        async with aiohttp.ClientSession() as session:
            async def send(data):
                if data:
                    async with session.post(url, data=data) as r:
                        await r.read()
                        return r.status
                else:
                    return 0
                
            async def get(channel):
                async with session.get(scu_api.address + '/devices/statusValue', params={'path': channel}) as r:
                    txt = await r.text()
                    r.raise_for_status()
                    return json.loads(txt)['value']
            
            while True:
                if self.is_stopped:
                    return
            
                if use_socket:
                    resp_post, (_, fields) = await asyncio.gather(send(self._data), gen.__anext__())
                    az, el = fields.values()
                else:
                    resp_post, az, el = await asyncio.gather(send(self._data), get(channels[0]), get(channels[1]))

                if self.is_stopped:
                   return
            
                assert resp_post in [0, 200], 'post failed'
                az = (180 - az) % 360 # stellarium az definition != mke az definition MKE 0 = North +90 = East
                self._data = {'az': np.deg2rad(az), 'alt': np.deg2rad(el)}
                
                self._tick_info(datetime.datetime.utcnow(), az, el)
                if verb:
                    print(self._info, end='\r')

if __name__ == "__main__":
    
    import sys
    args = sys.argv[1:]

    from mke_sculib.scu import scu as scu_api
    
    address = 'http://10.96.64.10:8080'
    # address = 'http://10.98.76.45:8997'
    # 'http://localhost:8080'

    if args:
        address = args[0]

    api = stellarium_api(scu_api(address), use_async=True, use_socket=True)
    api.run()



