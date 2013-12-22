#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import socket
import re

pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

TCP_IP = '192.168.1.50'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # normal = 1024, fast = 20

# Actual Maximums for HPI Servos
#servoMin = 100
#servoMax = 600

# 180degs Values
#servoMin = 150
#servoMid = 352
#servoMax = 600

# Steering Adjusted Maximums
steer_channel = 0
steer_Left = 470
steer_Center = 350
steer_Right = 245

# Brake Adjusted Maximums
brake_channel = 4
brake_On = 355
brake_Off = 400

# Throttle Adjusted Maximums
throt_channel = 8
throt_FullRev = 150
throt_Neutral = 350
throt_FullFor = 600

# Use command line arguments
#test_ch = int(sys.argv[1])
#test_freq = int(sys.argv[2])
#pwm.setPWM(test_ch, 0, test_freq)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
        conn, addr = s.accept()
        print "Connected to ", addr

        while 1:
           data = conn.recv(BUFFER_SIZE)
           if not data: break

           data = data.split(",")
	   print data
	   for packet in data:
              if len(packet) >= 5:
        	 pwm.setPWM(int(packet.split(".")[0]), 0, int(packet.split(".")[1]))
 
	print "Disconnected"
	pwm.setPWM(throt_channel, 0, throt_Neutral)
	pwm.setPWM(brake_channel, 0, brake_On)
	pwm.setPWM(steer_channel, 0, steer_Center)
