class BMP085 :
    def __init__(self):
        try:
            self.temp = 0
            self.pressure = 0
            self.alt = 0
        except:
            assert False, "Error: Failed to initialise sensor - BMP085" 


    def readTemperature(self):
        self.temp = 21
        return(self.temp)

    def readPressure(self):
        self.pressure = 1200
        return(self.pressure)

    def readAltitude(self):
        self.alt = 100
        return(self.alt)
