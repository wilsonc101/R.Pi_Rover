class PWM :
    def __init__(self, address=None, debug=None):
        try:
            self.address = address
            self.debug = debug
        except:
            assert False, "Error: Failed to initialise PWM"


    def setPWMFreq(self, freq):
        try:
            self.freq = freq
            return(True)

        except:
            return(False)


    def setPWM(self, channel, start, end):
        try:
            nothing = None
            return(True)

        except:
            return(False)
 
