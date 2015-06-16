class LSM303 :
    def __init__(self):
        self.accel = (0, 0, 0)
        self.magno = (0, 0, 0, 0)

    def read(self):
        self.accel = (1, 1, 1)
        self.magno = (10, 10, 10, 10)
        return(self.accel, self.magno)

