#!/usr/bin/python

import wx
import socket

class MainWindow(wx.Frame):
    def __init__(self,parent,id):
	
	net_connect()

	# Main Window
        wx.Frame.__init__(self,parent,id,'Pi Rover')

	# Global Events
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

	# Grid Builder
        sizer = wx.GridBagSizer(hgap=5, vgap=5)

	# Grid
	# ROW 1
	# Container for Throttle slider
        panel = wx.Panel(self, -1, (0,0), (70,220))
        grid_box = wx.StaticBox(panel, -1, 'throttle', size=(70, 220))
        self.slider_v = wx.Slider(panel, -1, 0, -100, 100, (0,20), (70, 180), wx.SL_VERTICAL | wx.SL_INVERSE)
        sizer.Add(panel, pos=(0,0), span=(4,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,3), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,4), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,5), flag=wx.EXPAND)

	# ROW 2
	# Col 1 + 2 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(1,2), flag=wx.EXPAND)

	# Mouse Capture panel
        panel = wx.Panel(self, -1, (0,0), (140,140))
        grid_box = wx.StaticBox(panel, -1, 'gimble', size=(140, 140))
        self.panel_gimble = wx.Panel(panel, -1, (20,20), (100,100))
        self.panel_gimble.Bind(wx.EVT_MOTION, self.MouseTrack_Cam)
        self.panel_gimble.SetBackgroundColour("light grey")
        sizer.Add(panel, pos=(1,3), span=(2,2))

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(1,5), flag=wx.EXPAND)


	# ROW 3
	# Col 1 + 2 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,2), flag=wx.EXPAND)

	# Col 4 + 5 spanned from ROW 2
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,5), flag=wx.EXPAND)


	# ROW 4
	# Col 1 + 2 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(3,2), flag=wx.EXPAND)
 
        panel = wx.Panel(self, -1, (0,0), (50,50))
        self.cb_mtrack = wx.CheckBox(panel, -1, 'Track Mouse')
	wx.EVT_CHECKBOX(self, self.cb_mtrack.GetId(), self.MouseClick_CamCB)
        sizer.Add(panel, pos=(3,3), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(3,4), flag=wx.EXPAND)
 
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(3,5), flag=wx.EXPAND)


	#ROW 5
	# Container for Direction slider	
        panel = wx.Panel(self, -1, (0,0), (500,60))
        grid_box = wx.StaticBox(panel, -1, 'direction', size=(500, 60))
        self.slider_h = wx.Slider(panel, -1, 0, -100, 100, (10,10), (480, 50), wx.SL_HORIZONTAL)
        sizer.Add(panel, pos=(4,0), span=(1,6), flag=wx.EXPAND)

	# End of Grid

        self.SetSizer(sizer)
        self.Fit()


	
    def OnKeyUp(self, event):
        key_translate(event.GetKeyCode())
	net_send("acc",frame.slider_v.GetValue())
	net_send("dir",frame.slider_h.GetValue())
        event.Skip()

    def MouseTrack_Cam(self, event):
	if self.cb_mtrack.GetValue() == True:
	        net_send("cam_x", event.GetX())
		net_send("cam_y", event.GetY())
	event.Skip()

    def MouseClick_CamCB(self, event):	
	toggle_mousetrack()
	event.Skip()



def net_connect():
	global net_socket

	HOST = '127.0.0.1'
	PORT = 5005
	net_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	net_socket.connect((HOST, PORT))

def net_disconnect():
	global net_socket

	net_socket.close()


def net_send(channel, value):
	global net_socket

        print(channel + "," + str(value) + ";")

	net_socket.sendall(channel + "," + str(value) + ";") 


def key_translate(keycode):
        global frame

        # Acc Up - W
        if keycode == 87:
                frame.slider_v.SetValue(frame.slider_v.GetValue() + 10)
        # Acc Down - S
        if keycode == 83:
                frame.slider_v.SetValue(frame.slider_v.GetValue() - 10)
        # Dir Right - D
        if keycode == 68:
                frame.slider_h.SetValue(frame.slider_h.GetValue() + 10)
        # Dir Left - A
        if keycode == 65:
                frame.slider_h.SetValue(frame.slider_h.GetValue() - 10)
        # STOP
        if keycode == wx.WXK_SPACE:
                frame.slider_v.SetValue(0)
                frame.slider_h.SetValue(0)
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
                net_send("cam_x", 50)
                net_send("cam_y", 50)


def load_window():
        global frame

        app=wx.PySimpleApp()
        frame=MainWindow(parent=None,id=-1)

        frame.Show()
        app.MainLoop()



# Start
load_window()
net_disconnect()






