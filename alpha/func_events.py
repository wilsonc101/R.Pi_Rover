import sys
import wx
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')


# Get servo names from config as arrays
servo_dir = [config.get('servos', 'direction_type'), config.get('servos', 'direction_name')]
servo_thr = [config.get('servos', 'throttle_type'), config.get('servos', 'throttle_name')]
servo_brk = [config.get('servos', 'brake_type'), config.get('servos', 'brake_name')]
servo_gim = [config.get('servos', 'gimbal_type'), config.get('servos', 'gimbal_name')]


# Bound Events (push event handler)
# Frame - Keyboard events
class Frame_KeyPress(wx.EvtHandler):
	def __init__(self):
		wx.EvtHandler.__init__(self)
		wx.EVT_KEY_UP(self, self.OnKeyUp)
	

	def OnKeyUp(self, event):
		keycode = int(event.GetKeyCode())
		frame = self.GetNextHandler()

	        # Acc Up - W
        	if keycode == 87:
                	frame.slider_v.SetValue(frame.slider_v.GetValue() + 10)
	                self.toggle_brake("set", "off")

	        # Acc Down - S
	        if keycode == 83:
	                frame.slider_v.SetValue(frame.slider_v.GetValue() - 10)
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

		print(int(servo_thr[0]),servo_thr[1],frame.slider_v.GetValue())
		print(int(servo_dir[0]),servo_dir[1],frame.slider_h.GetValue())


	def toggle_brake(self, function, state):
		frame = self.GetNextHandler()

	        if function == "toggle":
	                if frame.brk_state == False:
	                        frame.panel_brk.SetBackgroundColour("red")
#	                        net_send(0,"brk",0)
	                        frame.brk_state = True
	                        frame.slider_v.SetValue(0)
	                        frame.slider_h.SetValue(0)
				brk_value = 0
	                elif frame.brk_state == True:
	                        frame.panel_brk.SetBackgroundColour("green")
#	                        net_send(0,"brk",100)
	                        frame.brk_state = False
				brk_value = 100
	        elif function == "set":
	                if state == "on":
	                        frame.panel_brk.SetBackgroundColour("red")
#	                        net_send(0,"brk",0)
	                        frame.brk_state = True
	                        frame.slider_v.SetValue(0)
	                        frame.slider_h.SetValue(0)
				brk_value = 0
	                elif state == "off":
	                        frame.panel_brk.SetBackgroundColour("green")
#	                        net_send(0,"brk",100)
	                        frame.brk_state = False
				brk_value = 100

                print(int(servo_brk[0]),servo_brk[1],int(brk_value))


# 'Gimbal' panel mouse events
class Panel_TrackMouse(wx.EvtHandler):
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
				print(int(servo_gim[0]),servo_gim[1],(x*2)-100,(y*2)-100)	

	def OnDoubleLClick(self, event):
			print(int(servo_gim[0]),servo_gim[1],0,0)	# Send neutral






# Unbound Events (imported functions)
# Timer triggered keep-alive
def SendKeepAlive(event):
	print(99,"ka",0)
