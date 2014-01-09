import wx
import socket
import time

import controls_functions as event

class MainWindow(wx.Frame):
    def __init__(self,parent,id):

        # Main Window
        wx.Frame.__init__(self,parent,id,'Pi Rover')

        # Keep alive timer
        self.timer_ka = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, event.SendKeepAlive, self.timer_ka)     # Timer event uses an unbound function
        self.timer_ka.Start(2000)

        # Global Vars
        self.brk_state = False

        # Global Events
	self.PushEventHandler(event.Frame_AllEvents())			# Bind frame events to external hander (push)

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
	self.panel_gimble.PushEventHandler(event.Panel_GimbalTrack())		# Bind panel events to external handler (push)
        self.panel_gimble.SetBackgroundColour("light grey")
        sizer.Add(panel, pos=(1,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(1,3), flag=wx.EXPAND)


        # ROW 3
        # Col 1 + 2 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
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
	self.panel_brk.PushEventHandler(event.Panel_BrakeClick())		# Bind panel events to external handler (push)
#        self.panel_brk.Bind(wx.EVT_LEFT_UP, self.MouseClick_Brk)
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

