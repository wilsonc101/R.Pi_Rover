import wx
import socket
import time
import controls_functions as event


class MainWindow(wx.Frame):
    def __init__(self,parent,id):

        # Main Window
        wx.Frame.__init__(self,parent,id,'Pi Rover')
#        self.panel = wx.Panel(self, -1, (0,0), (500,500))
#        self.panel.SetBackgroundColour("white")


        # Keep alive timer
        self.timer_ka = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.TimerEvent, self.timer_ka)     # Timer event uses an unbound function
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

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(0,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (140,52))
        sizer.Add(panel, pos=(0,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(0,3), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(0,4), flag=wx.EXPAND)


        # ROW 2
        # Col 1 spanned from ROW 1

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(1,1), flag=wx.EXPAND)

        # Mouse Capture panel
        panel = wx.Panel(self, -1, (0,0), (140,140))
        grid_box = wx.StaticBox(panel, -1, 'gimble', size=(140, 140))
        self.panel_gimble = wx.Panel(panel, -1, (20,20), (100,100))
	self.panel_gimble.PushEventHandler(event.Panel_GimbalTrack())		# Bind panel events to external handler (push)
        self.panel_gimble.SetBackgroundColour("light grey")
        sizer.Add(panel, pos=(1,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(1,3), flag=wx.EXPAND)

	# Vehicle Guages
        panel = wx.Panel(self, -1, (0,0), (50,50))
        grid_box = wx.StaticBox(panel, -1, 'wifi', (0, 0), size=(172, 43))
	self.gauge_wifi = wx.Gauge(panel, -1, 100, (10, 16), (150, 20), wx.GA_HORIZONTAL, name="WiFi")
        grid_box = wx.StaticBox(panel, -1, 'battery - 1', (0, 46), size=(172, 43))
	self.gauge_batt_1 = wx.Gauge(panel, -1, 100, (10, 61), (150, 20), wx.GA_HORIZONTAL, name="Battery - 1")
        grid_box = wx.StaticBox(panel, -1, 'battery - 2', (0, 91), size=(172, 43))
	self.gauge_batt_2 = wx.Gauge(panel, -1, 100, (10, 106), (150, 20), wx.GA_HORIZONTAL, name="Battery - 2")
        sizer.Add(panel, pos=(1,4), flag=wx.EXPAND)

	self.gauge_wifi.SetValue(10)
	self.gauge_batt_1.SetValue(10)
	self.gauge_batt_2.SetValue(10)

	
        # ROW 3
        # Col 1 spanned from ROW 1

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(2,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(2,3), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(2,4), flag=wx.EXPAND)


        # ROW 4
        # Col 1 spanned from ROW 1
        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(3,1), flag=wx.EXPAND)

        # Container for brakes state
        panel = wx.Panel(self, -1, (0,0), (140,52))
        staticbox_brk = wx.StaticBox(panel, -1, 'brake', size=(140, 52))
        self.panel_brk = wx.Panel(panel, -1, (10,15), (120,30))
        self.panel_brk.SetBackgroundColour("green")
	self.panel_brk.PushEventHandler(event.Panel_BrakeClick())		# Bind panel events to external handler (push)
        sizer.Add(panel, pos=(3,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(3,3), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (50,50))
        sizer.Add(panel, pos=(3,4), flag=wx.EXPAND)


        #ROW 5
        # Container for Direction slider        
        panel = wx.Panel(self, -1, (0,0), (500,60))
        grid_box = wx.StaticBox(panel, -1, 'direction', size=(500, 60))
        self.slider_h = wx.Slider(panel, -1, 0, -100, 100, (10,10), (480, 50), wx.SL_HORIZONTAL | wx.SL_INVERSE)
        sizer.Add(panel, pos=(4,0), span=(1,5), flag=wx.EXPAND)

        # End of Grid

        self.SetSizer(sizer)
        self.Fit()

    def TimerEvent(self, evt):
	vehicle_data = event.SendKeepAlive(evt)
	self.UpdateGauges(vehicle_data)

    def UpdateGauges(self, vehicle_data):
	vehicle_metrics = vehicle_data.split(',')
        self.gauge_wifi.SetValue(int(vehicle_metrics[0]))
        self.gauge_batt_1.SetValue(int(vehicle_metrics[1]))
        self.gauge_batt_2.SetValue(int(vehicle_metrics[2]))

