import json
import threading
import time 


class gpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsdata = {'status': "NO FIX"}
    self.running = False
    self.fixmode = 3
 

  def setFixMode(self, mode):
      if 0 < mode < 3:
          self.fixmode = mode  

  def run(self):
    self.running = True
    while self.running:
        time.sleep(1)
        if self.fixmode > 1:
            self.gpsdata['status'] = "FIX"
            self.gpsdata['fixmode'] = self.fixmode
            self.gpsdata['latitude'] = 2.00000
            self.gpsdata['longitude'] = 51.20000
            self.gpsdata['time'] = "2015-01-01T12:00:00.000"
            self.gpsdata['speed'] = 0
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
