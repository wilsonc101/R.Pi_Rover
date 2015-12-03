import time


class LSM303 :
    def __init__(self):
        try:
            self.accel = (0, 0, 0)
            self.magno = (0, 0, 0, 0)
            self.acceldemodata = {'0':(0, 5, 0),
                              '1':(-10, 30, 0),
                              '2':(-20, 20, 0),
                              '3':(0, 0, 0),
                              '4':(30, -10, 0),
                              '5':(60, -40, 0),
                              '6':(70, 20, 0),
                              '7':(20, 0, 0),
                              '8':(10, 20, 0),
                              '9':(5, -10, 0)}
        except:
            assert False, "Error: Failed to initialise sensor - LSM303"


    def read(self):
        try:
            seconds = str(time.strftime("%S", time.gmtime()))[1:]
            x, y, z = self.acceldemodata[seconds]

            self.accel = (x, y, z)
            self.magno = (10, 10, 10, 10)

            return(self.accel, self.magno)

        except:
            return(False)

