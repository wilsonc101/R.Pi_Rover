#!/usr/bin/python

####### TIMER EVENT FOR KEEP ALIVE!! ##########

import wx
import socket
import time

class MainWindow(wx.Frame):
    def __init__(self,parent,id):

	# Main Window
        wx.Frame.__init__(self,parent,id,'Pi Rover')

	# Keep alive timer
        self.timer_ka = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.TimerEvent, self.timer_ka)
        self.timer_ka.Start(2000)

	# Global Vars
	self.brk_state = False

	# Global Events
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

	# Grid Builder
        sizer = wx.GridBagSizer(hgap=5, vgap=5)

	# Grid
	# ROW 1
	# Container for Throttle slider
        panel = wx.Panel(self, -1, (0,0), (70,305))
        grid_box = wx.StaticBox(panel, -1, 'throttle', size=(70, 305))
        self.slider_v = wx.Slider(panel, -1, 0, -100, 100, (0,20), (70, 275), wx.SL_VERTICAL | wx.SL_INVERSE)
        sizer.Add(panel, pos=(0,0), span=(4,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,1), flag=wx.EXPAND)

	# Container for net socket state
        panel = wx.Panel(self, -1, (0,0), (140,52))
        staticbox_conn = wx.StaticBox(panel, -1, 'connection', size=(140, 52))
	self.panel_connection = wx.Panel(panel, -1, (10,15), (120,30))
        self.panel_connection.SetBackgroundColour("grey")
        sizer.Add(panel, pos=(0,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,3), flag=wx.EXPAND)

	# ROW 2
	# Col 1 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(1,1), flag=wx.EXPAND)

	# Mouse Capture panel
        panel = wx.Panel(self, -1, (0,0), (140,140))
        grid_box = wx.StaticBox(panel, -1, 'gimble', size=(140, 140))
        self.panel_gimble = wx.Panel(panel, -1, (20,20), (100,100))
        self.panel_gimble.Bind(wx.EVT_MOTION, self.MouseTrack_Cam)
        self.panel_gimble.SetBackgroundColour("light grey")
        sizer.Add(panel, pos=(1,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(1,3), flag=wx.EXPAND)


	# ROW 3
	# Col 1 + 2 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,1), flag=wx.EXPAND)

	# Container for mouse track checkbox
        panel = wx.Panel(self, -1, (0,0), (50,50))
        self.cb_mtrack = wx.CheckBox(panel, -1, 'track mouse')
	wx.EVT_CHECKBOX(self, self.cb_mtrack.GetId(), self.MouseClick_CamCB)
        sizer.Add(panel, pos=(2,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,3), flag=wx.EXPAND)


	# ROW 4
	# Col 1 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(3,1), flag=wx.EXPAND)
 
	# Container for brakes state
        panel = wx.Panel(self, -1, (0,0), (140,52))
        staticbox_brk = wx.StaticBox(panel, -1, 'brake', size=(140, 52))
	self.panel_brk = wx.Panel(panel, -1, (10,15), (120,30))
        self.panel_brk.SetBackgroundColour("green")
        self.panel_brk.Bind(wx.EVT_LEFT_UP, self.MouseClick_Brk)
        sizer.Add(panel, pos=(3,2), flag=wx.EXPAND)
	
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(3,3), flag=wx.EXPAND)
 

	#ROW 5
	# Container for Direction slider	
        panel = wx.Panel(self, -1, (0,0), (500,60))
        grid_box = wx.StaticBox(panel, -1, 'direction', size=(500, 60))
        self.slider_h = wx.Slider(panel, -1, 0, -100, 100, (10,10), (480, 50), wx.SL_HORIZONTAL)
        sizer.Add(panel, pos=(4,0), span=(1,4), flag=wx.EXPAND)

	# End of Grid

        self.SetSizer(sizer)
        self.Fit()


	
    def OnKeyUp(self, event):
        key_translate(event.GetKeyCode())
	net_send(0,"thr",frame.slider_v.GetValue())
	net_send(0,"dir",frame.slider_h.GetValue())
        event.Skip()

    def MouseTrack_Cam(self, event):
	if self.cb_mtrack.GetValue() == True:
	        net_send(1,"gim",event.GetX(),event.GetY())
	event.Skip()

    def MouseClick_CamCB(self, event):	
	toggle_mousetrack()
	event.Skip()

    def MouseClick_Brk(self, event):
	toggle_brake("toggle","na")
	net_send(0,"thr",frame.slider_v.GetValue())
	net_send(0,"dir",frame.slider_h.GetValue())

    def FrameUpdate(self):
	self.Update()
	self.Refresh()

    def TimerEvent(self, event):
	net_send(3,"ka",0)


def net_connect():
	global net_socket, net_socket_state, frame

	HOST = '127.0.0.1'
	PORT = 5005
	net_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	net_socket_state = False

	while net_socket_state == False:
		try:
			net_socket.connect((HOST, PORT)) 
			net_socket_state = True
		        frame.panel_connection.SetBackgroundColour("green")
			frame.FrameUpdate()

		except:
			print("Network Connection Failed")
			net_socket_state = False
		        frame.panel_connection.SetBackgroundColour("red")
			frame.FrameUpdate()
			time.sleep(2)


def net_disconnect():
	global net_socket

	net_socket.close()


def net_send(type,channel,value1,value2=0):
	global net_socket

	try:
		net_socket.sendall(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";") 
		print(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";") 
	except:
		print("Network Connection Error - Transmit")	
		net_connect()

	

def key_translate(keycode):
        global frame

        # Acc Up - W
        if keycode == 87:
                frame.slider_v.SetValue(frame.slider_v.GetValue() + 10)
		toggle_brake("set", "off")
        # Acc Down - S
        if keycode == 83:
                frame.slider_v.SetValue(frame.slider_v.GetValue() - 10)
		toggle_brake("set", "off")
        # Dir Right - D
        if keycode == 68:
                frame.slider_h.SetValue(frame.slider_h.GetValue() + 10)
        # Dir Left - A
        if keycode == 65:
                frame.slider_h.SetValue(frame.slider_h.GetValue() - 10)
        # STOP - Space
        if keycode == wx.WXK_SPACE:
                frame.slider_v.SetValue(0)
                frame.slider_h.SetValue(0)
		toggle_brake("toggle", "na")
        # Toggle Mouse Track - M
        if keycode == 77:
		if frame.cb_mtrack.GetValue() == True:
			frame.cb_mtrack.SetValue(False)
		else:
			frame.cb_mtrack.SetValue(True)
		toggle_mousetrack()
		

def toggle_mousetrack():
        global frame

        if frame.cb_mtrack.GetValue() == True:
                frame.panel_gimble.SetBackgroundColour("white")
        elif frame.cb_mtrack.GetValue() == False:
                frame.panel_gimble.SetBackgroundColour("light grey")
                net_send(1,"gim",0,0)

def toggle_brake(function, state):
	global frame
	if function == "toggle": 
		if frame.brk_state == False:
		        frame.panel_brk.SetBackgroundColour("red")
			net_send(0,"brk",100)
			frame.brk_state = True
                	frame.slider_v.SetValue(0)
        	        frame.slider_h.SetValue(0)
		elif frame.brk_state == True:		
		        frame.panel_brk.SetBackgroundColour("green")
			net_send(0,"brk",0)
			frame.brk_state = False
	elif function == "set":
		if state == "on":
		        frame.panel_brk.SetBackgroundColour("red")
			net_send(0,"brk",100)
			frame.brk_state = True
                	frame.slider_v.SetValue(0)
        	        frame.slider_h.SetValue(0)
		elif state == "off":
		        frame.panel_brk.SetBackgroundColour("green")
			net_send(0,"brk",0)
			frame.brk_state = False


def load_window():
        global frame, net_socket_state

        app=wx.PySimpleApp()

	frame=MainWindow(parent=None,id=-1)
	net_connect()

        frame.Show()
        app.MainLoop()




# Start
load_window()

net_disconnect()






