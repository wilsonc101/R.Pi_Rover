import sys
import wx
import ConfigParser
import time

import controls_network as network
import controls_logging as log


config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

logfile = log.CreateLogger(console=1, file=1, filepath='pi_rover.log', level=config.get('logging', 'level'))


# Get servo names from config as arrays
servo_dir = [config.get('servos', 'direction_type'), config.get('servos', 'direction_name')]
servo_thr = [config.get('servos', 'throttle_type'), config.get('servos', 'throttle_name')]
servo_brk = [config.get('servos', 'brake_type'), config.get('servos', 'brake_name')]
servo_gim = [config.get('servos', 'gimbal_type'), config.get('servos', 'gimbal_name')]

# Init network connection
logfile.info('connecting to vehicle')
socket = network.net_connect()


### Bound Events (push event handler)
# Frame - Keyboard events
class Frame_AllEvents(wx.EvtHandler):
	def __init__(self):
		wx.EvtHandler.__init__(self)
		wx.EVT_KEY_UP(self, self.OnKeyUp)
		wx.EVT_SCROLL_CHANGED(self, self.OnSliderChange)


	# Catch slider changes
	def OnSliderChange(self, event):
		frame = self.GetNextHandler()

		self.toggle_brake("set", "off")

		network.net_send(socket,int(servo_thr[0]),servo_thr[1],frame.slider_v.GetValue())
		network.net_send(socket,int(servo_dir[0]),servo_dir[1],frame.slider_h.GetValue())
		logfile.debug('net send - sliders - ' + str(frame.slider_v.GetValue()) + str(frame.slider_h.GetValue()))
		

	# Catch all key presses
	def OnKeyUp(self, event):
		frame = self.GetNextHandler()
		keycode = int(event.GetKeyCode())
	
	        # Acc Up - W
        	if keycode == 87:
                	frame.slider_v.SetValue(frame.slider_v.GetValue() + 5)
	                self.toggle_brake("set", "off")

	        # Acc Down - S
	        if keycode == 83:
	                frame.slider_v.SetValue(frame.slider_v.GetValue() - 5)
	                self.toggle_brake("set", "off")
	
	        # Dir Right Step - D
	        if keycode == 68:
	                frame.slider_h.SetValue(frame.slider_h.GetValue() - 10)
	
	        # Dir Right Full - E
	        if keycode == 69:
	                if frame.slider_h.GetValue() == -100:
		                frame.slider_h.SetValue(0)
			else:
		                frame.slider_h.SetValue(-100)
			

	        # Dir Left Step  - A
	        if keycode == 65:
	                frame.slider_h.SetValue(frame.slider_h.GetValue() + 10)
	
	        # Dir Left Full - E
	        if keycode == 81:
	                if frame.slider_h.GetValue() == 100:
		                frame.slider_h.SetValue(0)
			else:
		                frame.slider_h.SetValue(100)

	        # Dir Center - 2
	        if keycode == 50:
	                frame.slider_h.SetValue(0)
	
	        # STOP - Space
	        if keycode == wx.WXK_SPACE:
	                frame.slider_v.SetValue(0)
	                frame.slider_h.SetValue(0)
	                self.toggle_brake("toggle", "na")

		network.net_send(socket,int(servo_thr[0]),servo_thr[1],frame.slider_v.GetValue())
		network.net_send(socket,int(servo_dir[0]),servo_dir[1],frame.slider_h.GetValue())
		logfile.debug('net send - sliders - ' + str(frame.slider_v.GetValue()) + str(frame.slider_h.GetValue()))
	
	
	# Toggle brake on key or slider events
	def toggle_brake(self, function, state):
		frame = self.GetNextHandler()

	        if function == "toggle":
	                if frame.brk_state == False:
	                        frame.panel_brk.SetBackgroundColour("red")
	                        frame.brk_state = True
	                        frame.slider_v.SetValue(0)
	                        frame.slider_h.SetValue(0)
				brk_value = 0
	                elif frame.brk_state == True:
	                        frame.panel_brk.SetBackgroundColour("green")
	                        frame.brk_state = False
				brk_value = 100
	        elif function == "set":
	                if state == "on":
	                        frame.panel_brk.SetBackgroundColour("red")
	                        frame.brk_state = True
	                        frame.slider_v.SetValue(0)
	                        frame.slider_h.SetValue(0)
				brk_value = 0
	                elif state == "off":
	                        frame.panel_brk.SetBackgroundColour("green")
	                        frame.brk_state = False
				brk_value = 100

                network.net_send(socket,int(servo_brk[0]),servo_brk[1],int(brk_value))
		logfile.debug('net send - break - ' + str(brk_value))


# 'Gimbal' panel mouse events
class Panel_GimbalTrack(wx.EvtHandler):
	def __init__(self):
        	wx.EvtHandler.__init__(self)
                wx.EVT_MOTION(self, self.OnMouseMove)
		wx.EVT_LEFT_DCLICK(self, self.OnDoubleLClick)
	
	# Output cords when left-click-drag over panel
	def OnMouseMove(self, event):
		x = 100 - int(event.GetX())
		y = int(event.GetY())

		if event.LeftIsDown() is True:				# Only send cords when left mouse is held
			if 0 <= x <= 100 and 0 <= y <= 100:
				# Convert 0-100 to -100-100 and send
				network.net_send(socket,int(servo_gim[0]),servo_gim[1],(x*2)-100,(y*2)-100)
				logfile.debug('net send - gimbal - ' + str((x*2)-100) + str((y*2)-100))

	# Set to neutral position on double-click
	def OnDoubleLClick(self, event):
			network.net_send(socket,int(servo_gim[0]),servo_gim[1],0,0)	# Send neutral
			logfile.debug('net send - gimbal - 0, 0')


# Release break on mouse-panel click
class Panel_BrakeClick(wx.EvtHandler):
        def __init__(self):
                wx.EvtHandler.__init__(self)
                wx.EVT_LEFT_UP(self, self.OnLClickUp)

        def OnLClickUp(self, event):
                panel = self.GetNextHandler()

		# Sent brake as 'off' - cannot be used to set as on as no throttle control here
		panel.SetBackgroundColour("green")
		network.net_send(socket,int(servo_brk[0]),servo_brk[1],100)
		logfile.debug('net send - break - 100')


# Send 'shutdown' packet to vehicle on button press
class Button_ShutdownVehicle(wx.EvtHandler):
        def __init__(self):
		wx.EvtHandler.__init__(self)
		wx.EVT_LEFT_UP(self, self.OnClick)

	def OnClick(self, event):
		network.net_send(socket,98,"sd",0)
		logfile.debug('net send - shutdown - 0')
		logfile.warning('sent vehicle shutdown')
		event.Skip()




###  Unbound Events (imported functions)
# Timer triggered keep-alive (2s)
def SendKeepAlive(event):
	# Keep alive performs three functions:
	# 1) Send constant stream of traffic to avoid network session timeout/sleep
	# 2) Result of sending 'KA' used to check socket is still valid
	# 3) Triggers vehicle to return status details (e.g battery state) - 'return' value
	NetCheck(network.net_send(socket,99,"ka",0))
	logfile.debug('net send - keepalive - 0')
	
	# Also use returned data to validate socket
	vehicle_data = network.net_listen(socket)
	logfile.debug('net listen - vehicle data - ' + str(vehicle_data))

	if vehicle_data != "False":
		return(vehicle_data)
	else:
		NetCheck(vehicle_data)



### Internal functions - used by events/functions within this file
# Check result of keep-alive, prompt if connection has failed
def NetCheck(result):
	global socket

	if result == "False":
		logfile.warning('vehicle connection failed')
		socket = None		# Wipe out old socket

		answer = 0
	        answer = wx.MessageBox('Network connection has failed - reconnect?', 'Connection Failure', wx.YES_NO | wx.ICON_EXCLAMATION)
		while answer == 0: time.sleep(0.2)

		if answer == 8:
			logfile.warning('user closed controls after network failure')
			raise SystemExit("Pi Rover manually exited after network failure")
       		elif answer == 2:
			print("Retrying Connection")
			logfile.warning('retrying vehicle connection')
			socket = network.net_connect()
	


	
