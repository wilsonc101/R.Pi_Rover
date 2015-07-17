#!/usr/bin/python -B

from PyQt4 import QtCore, QtGui
import sys

import class_gui


if __name__ == '__main__':
    gui_app = QtGui.QApplication(sys.argv)
    gui_mainwindow = QtGui.QMainWindow()
    gui = class_gui.Ui_MainWindow()
    gui.setupUi(gui_mainwindow)
    gui_mainwindow.show()
    sys.exit(gui_app.exec_())
    print("here")
