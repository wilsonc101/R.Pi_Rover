#!/usr/bin/python -B

from PyQt4 import QtCore, QtGui

import class_gui
import sys

if __name__ == '__main__':
    try:
        gui_app = QtGui.QApplication(sys.argv)
        gui_mainwindow = QtGui.QMainWindow()
        gui = class_gui.Ui_MainWindow()
        gui.setupUi(gui_mainwindow)
        gui_mainwindow.show()
        sys.exit(gui_app.exec_())

    except Exception, e:
        print "Exiting...."
