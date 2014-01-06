import sys
import wx
import ConfigParser

import controls_network as network

config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')


# Get servo names from config as arrays
servo_dir = [config.get('servos', 'direction_type'), config.get('servos', 'direction_name')]
servo_thr = [config.get('servos', 'throttle_type'), config.get('servos', 'throttle_name')]
servo_brk = [config.get('servos', 'brake_type'), config.get('servos', 'brake_name')]
servo_gim = [config.get('servos', 'gimbal_type'), config.get('servos', 'gimbal_name')]

# Init network connection
socket = network.net_connect()


# Bound Events (push event handler)
# Frame - Keyboard events
class Frame_KeyPress(wx.EvtHandler):
	def __init__(self):
		wx.EvtHandler.__init__(self)
		wx.EVT_KEY_UP(self, self.OnKeyUp)
		wx.EVT_SCROLL_CHANGED(self, self.OnSliderChange)

	def OnSliderChange(self, event):
		frame = self.GetNextHandler()

		self.toggle_brake("set", "off")

		network.net_send(socket,int(servo_thr[0]),servo_thr[1],frame.slider_v.GetValue())
		network.net_send(socket,int(servo_dir[0]),servo_dir[1],frame.slider_h.GetValue())


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
	                frame.slider_h.SetValue(frame.slider_h.GetValue() + 10)
	
	        # Dir Right Full - E
	        if keycode == 69:
	                frame.slider_h.SetValue(100)

	        # Dir Left Step  - A
	        if keycode == 65:
	                frame.slider_h.SetValue(frame.slider_h.GetValue() - 10)
	
	        # Dir Left Full - E
	        if keycode == 81:
	                frame.slider_h.SetValue(-100)
	
	        # STOP - Space
	        if keycode == wx.WXK_SPACE:
	                frame.slider_v.SetValue(0)
	                frame.slider_h.SetValue(0)
	                self.toggle_brake("toggle", "na")

		network.net_send(socket,int(servo_thr[0]),servo_thr[1],frame.slider_v.GetValue())
		network.net_send(socket,int(servo_dir[0]),servo_dir[1],frame.slider_h.GetValue())


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


# 'Gimbal' panel mouse events
class Panel_GimbalTrack(wx.EvtHandler):
	def __init__(self):
        	wx.EvtHandler.__init__(self)
                wx.EVT_MOTION(self, self.OnMouseMove)
		wx.EVT_LEFT_DCLICK(self, self.OnDoubleLClick)
	
	def OnMouseMove(self, event):
		x = int(event.GetX())
		y = int(event.GetY())

		if event.LeftIsDown() is True:				# Only send cords when left mouse is held
			if 0 <= x <= 100 and 0 <= y <= 100:
				# Convert 0-100 to -100-100 and send
				network.net_send(socket,int(servo_gim[0]),servo_gim[1],(x*2)-100,(y*2)-100)	

	def OnDoubleLClick(self, event):
			network.net_send(socket,int(servo_gim[0]),servo_gim[1],0,0)	# Send neutral



class Panel_BrakeClick(wx.EvtHandler):
        def __init__(self):
                wx.EvtHandler.__init__(self)
                wx.EVT_LEFT_UP(self, self.OnLClickUp)

        def OnLClickUp(self, event):
                panel = self.GetNextHandler()

		# Sent brake as 'off' - cannot be used to set as on as no throttle control here
		panel.SetBackgroundColour("green")
		network.net_send(socket,int(servo_brk[0]),servo_brk[1],100)




# Unbound Events (imported functions)
# Timer triggered keep-alive
def SendKeepAlive(event):
	network.net_send(socket,99,"ka",0)


