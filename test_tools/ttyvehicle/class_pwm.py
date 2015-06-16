class PWM :
    def __init__(self, address=None, debug=None):
        self.address = address
        self.debug = debug

    def setPWMFreq(self, freq):
        self.freq = freq

    def setPWM(self, channel, start, end):
        nothing = None
#        print (str(channel) + " - " + str(start) + "," + str(end))
 
