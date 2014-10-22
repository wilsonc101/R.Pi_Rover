import wx
import asyncore

import vsim_functions as vsim


class MainWindow(wx.Frame):
    def __init__(self,parent,id):

        # Main Window
        wx.Frame.__init__(self,parent,id,'Pi Rover - Sim')
#        self.panel = wx.Panel(self, -1, (0,0), (600,600))
#        self.panel.SetBackgroundColour("white")

	# Asyncore poller/timer
	self.timer_poll = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.TimerEvent, self.timer_poll)
	self.timer_poll.Start(20)

        # Grid Builder
        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        # Grid
        # ROW 1
        panel = wx.Panel(self, -1, (0,0), (100,100))
        self.static_text_1 = wx.StaticText(panel, -1, 'Vehicle')
        self.static_text_1.SetForegroundColour('blue')
        sizer.Add(panel, pos=(0,0), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'T.Pos', size=(100, 100))
        self.tpos_text = wx.StaticText(panel, -1,  '0.0', pos=(5,40))
        sizer.Add(panel, pos=(0,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'D.Pos', size=(100, 100))
        self.dpos_text = wx.StaticText(panel, -1,  '0.0', pos=(5,40))
        sizer.Add(panel, pos=(0,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'Brake', size=(100, 100))
        self.brake_text = wx.StaticText(panel, -1,  '0.0', pos=(5,40))
        sizer.Add(panel, pos=(0,3), flag=wx.EXPAND)

		
	# ROW 2
        panel = wx.Panel(self, -1, (0,0), (100,100))
        self.static_text_2 = wx.StaticText(panel, -1, 'Gimble')
        self.static_text_2.SetForegroundColour('blue')
        sizer.Add(panel, pos=(1,0), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'X.Pos', size=(100, 100))
        self.gimx_text = wx.StaticText(panel, -1,  '0.0', pos=(5,40))
        sizer.Add(panel, pos=(1,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'Y.Pos', size=(100, 100))
        self.gimy_text = wx.StaticText(panel, -1,  '0.0', pos=(5,40))
        sizer.Add(panel, pos=(1,2), flag=wx.EXPAND)

		
	# ROW 3
        panel = wx.Panel(self, -1, (0,0), (100,100))
        self.static_text_2 = wx.StaticText(panel, -1, 'Data')
        self.static_text_2.SetForegroundColour('red')
        sizer.Add(panel, pos=(2,0), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'WiFi', size=(100, 100))
        self.slider_wifi = wx.Slider(panel, -1, 0, 0, 100, (10,10), (75, 80), wx.SL_HORIZONTAL)
        sizer.Add(panel, pos=(2,1), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'Bat.1', size=(100, 100))
        self.slider_bat1 = wx.Slider(panel, -1, 0, 0, 100, (10,10), (75, 80), wx.SL_HORIZONTAL)
        sizer.Add(panel, pos=(2,2), flag=wx.EXPAND)

        panel = wx.Panel(self, -1, (0,0), (100,100))
        grid_box = wx.StaticBox(panel, -1, 'Bat.2', size=(100, 100))
        self.slider_bat2 = wx.Slider(panel, -1, 0, 0, 100, (10,10), (75, 80), wx.SL_HORIZONTAL)
        sizer.Add(panel, pos=(2,3), flag=wx.EXPAND)


	dispatchserver = vsim.DispatchServer(self)

        self.SetSizer(sizer)
        self.Fit()

    def TimerEvent(self, evt):
        asyncore.poll()
