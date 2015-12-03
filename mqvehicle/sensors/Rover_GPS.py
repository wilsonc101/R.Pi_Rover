import json
import threading

from gps import *

class gpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE)
        self.gpsdata = {'status': "NO FIX"}
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.gpsd.next()
            # This will continue to loop and grab EACH
            # set of gpsd info to clear the buffer
            if self.gpsd.fix.mode > 1:
                self.gpsdata['status'] = "FIX"
                self.gpsdata['fixmode'] = self.gpsd.fix.mode
                self.gpsdata['latitude'] = self.gpsd.fix.latitude
                self.gpsdata['longitude'] = self.gpsd.fix.longitude
                self.gpsdata['time'] = self.gpsd.utc
                self.gpsdata['speed'] = self.gpsd.fix.speed
                self.gpsdata['altitude'] = self.gpsd.fix.altitude
                self.gpsdata['climb'] = self.gpsd.fix.climb
                self.gpsdata['error-speed'] = self.gpsd.fix.eps
                self.gpsdata['error-latitude'] = self.gpsd.fix.epx
                self.gpsdata['error-longitude'] = self.gpsd.fix.epy
                self.gpsdata['error-altitude'] = self.gpsd.fix.epv
                self.gpsdata['error-time'] = self.gpsd.fix.ept
                self.gpsdata['satellites'] = str(self.gpsd.satellites)
            else:
                self.gpsdata['status'] = "NO FIX"

if __name__ == '__main__':
    gpsp = gpsPoller()
    try:
        gpsp.start()
        while True:
            if gpsp.gpsdata['status'] == "FIX":
                print json.dumps(gpsp.gpsdata)
            else:
                print gpsp.gpsdata['status']

    except (KeyboardInterrupt, SystemExit):
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing

