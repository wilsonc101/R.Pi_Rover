class LSM303 :
    def __init__(self):
        self.accel = (0, 0, 0)
        self.magno = (0, 0, 0, 0)
        self.acceldemodata = {'0':(0,5,0),
                              '1':(10,30,0),
                              '2':(20,20,0),
                              '3':(30,0,0),
                              '4':(30,10,0),
                              '5':(60,40,0),
                              '6':(70,20,0),
                              '7':(20,0,0),
                              '8':(10,20,0),
                              '9':(5,10,0)}



    def read(self):


        self.accel = (1, 1, 1)
        self.magno = (10, 10, 10, 10)
        return(self.accel, self.magno)

