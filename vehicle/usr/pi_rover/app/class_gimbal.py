# Gimbal class
# Dependant on 'class_servo' for 'StandardServo' definiation

from __future__ import division
import class_servo as servo


class XYGimbal():
	# Simple 2-servo gimbal, X & Y axis
        def __init__(self,(xchannelid,xmin,xmax,xneutral,xname),(ychannelid,ymin,ymax,yneutral,yname),name):
                self.XServo = servo.StandardServo(xchannelid,xmin,xmax,xneutral,xname)
                self.YServo = servo.StandardServo(ychannelid,ymin,ymax,yneutral,yname)
		self.Name = name

        def Translate(self,xinput,yinput):
                # Translate percentages to interpolated outputs
                # Input is expected to be -100 to 100 (full reverse to full forward)

		x_output = self.XServo.Translate(xinput)
		y_output = self.YServo.Translate(yinput)
	
                return (x_output,y_output)


# Examples:
# Define gimbal - ((x axis channel id, min, max, neutral),(y axis channel id, min, max, neutral))
# gimbal = XYGimbal((3,100,200,150),(4,-100,100,0))
#
# Translate %age to real PWM figures - (x axis -100 to 100, y axis -100 to 100)
# print(gimbal.Translate(-100,100))

