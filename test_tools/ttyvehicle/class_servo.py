#!/usr/bin/python
from __future__ import division


class StandardServo():
    def __init__(self,channelid,min,max,neutral,name):
        try:
            self.Channel = int(channelid)
            self.RealMin = int(min)
            self.RealMax = int(max)
            self.RealNeutral = int(neutral)
            self.Name = name

        except:
            assert False, "Error: Failed to initialise server"

    
    def Translate(self, inputper):
        # Translate percentages to interpolated outputs
        # Input is expected to be -100 to 100 (full reverse to full forward)
        try:
            inputper = int(inputper)
    
            output = self.RealNeutral
    
            if inputper >= -100 and inputper <= 100:
                if inputper < 0:
                    neg_span = abs(self.RealNeutral-self.RealMin)
                    output = self.RealNeutral - ((neg_span / 100)*abs(inputper))
                elif inputper > 0:
                    pos_span = abs(self.RealNeutral-self.RealMax)
                    output = self.RealNeutral + ((pos_span / 100)*abs(inputper))

            return output

        except:
            return(False)


# Examples:
# Define server - (channel id, min, max, neutral)
# servo = StandardServo(0,100,200,120)
#
# Translate %age to real PWM figure - (-100 to 100)
# print(servo.Translate(-24))


# Specific servo details:

# HPI Standard Servos
#servoMin = 100
#servoMax = 600
#
# 180degs Values
#servoMin = 150
#servoMid = 352
#servoMax = 600

