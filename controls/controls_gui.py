import wx
import socket
import time
import controls_functions as event

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')


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
        self.slider_v = wx.Slider(panel, -1, 0, -100, 100, (0,20), (70, 275), wx.SL_LABELS | wx.SL_VERTICAL | wx.SL_INVERSE)
        sizer.Add(panel, pos=(0,0), span=(4,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (20,50))
        sizer.Add(panel, pos=(0,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (140,52))
        self.thr_limit_text = wx.StaticText(panel, -1, '', (0,10), (0,0), wx.ALIGN_CENTER)
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
        self.wifi_grid_box = wx.StaticBox(panel, -1, 'wifi', (0, 0), size=(172, 43))
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
        grid_box = wx.StaticBox(panel, -1, 'vehicle reply (ms)', (0, 0), size=(172, 50))
        self.response_text = wx.StaticText(panel, -1,  '0', pos=(5,20))
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
	self.button_poweroff = wx.Button(panel, -1, 'Shutdown Vehicle', (20, 15))
	self.button_poweroff.PushEventHandler(event.Button_ShutdownVehicle())
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
	vehicle_data, response_time = event.SendKeepAlive(evt)
	self.UpdateGauges(vehicle_data, response_time)
	self.LimitControls(vehicle_data, response_time)


    def UpdateGauges(self, vehicle_data, response_time):
	vehicle_metrics = vehicle_data.split(',')
        self.gauge_wifi.SetValue(int(vehicle_metrics[0]))
        self.gauge_batt_1.SetValue(int(vehicle_metrics[1]))
        self.gauge_batt_2.SetValue(int(vehicle_metrics[2]))
        self.response_text.SetLabel(str(response_time))

    def LimitControls(self, vehicle_data, response_time):
        
        wifi_value = vehicle_data.split(',')[0]
	min_wifi_value = int(config.get('limits', 'min_wifi_value'))
        max_response_time = int(config.get('limits', 'max_ka_response_time'))

        limited_throttle_value = int(self.slider_v.GetValue())/2


        # Limit throttle input when network conditions are poor
        if int(wifi_value) <= min_wifi_value or int(response_time) >= max_response_time:

             if self.slider_v.GetMax() != 50:
               self.slider_v.SetValue(limited_throttle_value)

             self.slider_v.SetRange(-50,50)

	     wx_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
	     self.thr_limit_text.SetLabel('THROTTLE\nLIMITED')
	     self.thr_limit_text.SetForegroundColour('red')
	     self.thr_limit_text.SetFont(wx_font)

             if int(response_time) >= max_response_time:
               self.response_text.SetForegroundColour('red')
             else:
               self.response_text.SetForegroundColour('black')

             if int(wifi_value) <= min_wifi_value:
               self.wifi_grid_box.SetForegroundColour('red')
             else:
               self.wifi_grid_box.SetForegroundColour('black')

             event.SetThrottleInputLimit(self)
             
        else:
             self.slider_v.SetRange(-100,100)
	     self.thr_limit_text.SetLabel('')
             self.response_text.SetForegroundColour('black')
             self.wifi_grid_box.SetForegroundColour('black')


