import threading
import time

import sim_data as data


class gpsPoller(threading.Thread):
    def __init__(self):
        try:
            threading.Thread.__init__(self)
            self.gpsdata = {'status': "NO FIX"}
            self.running = False
            self.fixmode = 3

            self.gps_cords = data.gps_cords
            self._count_gps_cords = len(self.gps_cords)
            self._count = 100

        except:
            assert False, "Error: Failed to initialise GPS thread"


    def setFixMode(self, mode):
        try:
            if 0 < mode < 3:
                self.fixmode = mode
            return True

        except:
            return False


    def run(self):
        try:
            self.running = True

            while self.running:
                time.sleep(1)

                # Reset counter
                if self._count > (self._count_gps_cords - 1): 
                    self._count = 0

                latitude, longitude = self.gps_cords[self._count]
                self._count += 1

                if self.fixmode > 1:
                    self.gpsdata['status'] = "FIX"
                    self.gpsdata['fixmode'] = self.fixmode
                    self.gpsdata['latitude'] = str(latitude).ljust(9, "0")
                    self.gpsdata['longitude'] = str(longitude).ljust(9, "0")
                    self.gpsdata['time'] = "2015-01-01T12:00:00.000"
                    self.gpsdata['speed'] = 10
                    self.gpsdata['altitude'] = 120
                    self.gpsdata['climb'] = 0
                    self.gpsdata['error-speed'] = 0
                    self.gpsdata['error-latitude'] = 0
                    self.gpsdata['error-longitude'] = 0
                    self.gpsdata['error-altitude'] = 0
                    self.gpsdata['error-time'] = 0
                    self.gpsdata['satellites'] = "unknown"

                else:
                    self.gpsdata['status'] = "NO FIX"

        except:    
            assert False, "Error: Processing GPS data failed"
