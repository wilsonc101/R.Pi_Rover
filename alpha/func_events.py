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
		print(int(event.GetKeyCode()))



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
