#!/usr/bin/python

import wx
import sys

import gui_controls as gui


def load_window():
        app=wx.PySimpleApp()
        frame=gui.MainWindow(parent=None,id=-1)
        frame.Show()
        app.MainLoop()



load_window()

