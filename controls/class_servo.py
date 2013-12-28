#!/usr/bin/python
from __future__ import division

class StandardServo():
	def __init__(self,channelid,min,max,neutral):
		self.Channel = channelid
		self.RealMin = min
		self.RealMax = max
		self.RealNeutral = neutral

	def Translate(self, input):
		# Translate percentages to interpolated outputs
		# Input is expected to be -100 to 100 (full reverse to full forward)
	
		output = self.RealNeutral

		if input >= -100 and input <= 100:
			if input < 0:
				neg_span = abs(self.RealNeutral-self.RealMin)
				output = self.RealNeutral - ((neg_span / 100)*abs(input))
			elif input > 0:
				pos_span = abs(self.RealNeutral-self.RealMax)
				output = self.RealNeutral + ((pos_span / 100)*abs(input))
		else:
			output = "out of range"
				
		return output


# Examples:
# Define server - (channel id, min, max, neutral)
# servo = StandardServo(0,100,200,120)
#
# Translate %age to real PWM figure - (-100 to 100)
# print(servo.Translate(-24))
