import json
import threading
import time 

class gpsPoller(threading.Thread):
  def __init__(self):
    try:
        threading.Thread.__init__(self)
        self.gpsdata = {'status': "NO FIX"}
        self.running = False
        self.fixmode = 3
        self.demodata = {'2':(51.449501, -2.146074),
                    '3':(51.449501, -2.146074),
                    '4':(51.448806, -2.145816),
                    '5':(51.448806, -2.145816),
                    '6':(51.448298, -2.146085),
                    '7':(51.448298, -2.146085),
                    '8':(51.448659, -2.146460),
                    '9':(51.448659, -2.146460),
                    '0':(51.449147, -2.146600),
                    '1':(51.449147, -2.146600)}
    except:
      assert False, "Error: Failed to initialise GPS thread"


  def setFixMode(self, mode):
    try:
        if 0 < mode < 3:
            self.fixmode = mode  
        return(True)

    except:
        return(False)


  def run(self):
    try:
        self.running = True
        while self.running:
            time.sleep(1)
            seconds = str(time.strftime("%S", time.gmtime()))[1:]
            latitude, longitude = self.demodata[seconds]
        
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
