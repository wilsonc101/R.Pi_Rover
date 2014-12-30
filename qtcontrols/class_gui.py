# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pirover_controls.ui'
#
# Created: Fri Dec 26 18:10:36 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import json

import class_workers as workers



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(553, 463)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame_controls = QtGui.QFrame(self.centralwidget)
        self.frame_controls.setGeometry(QtCore.QRect(0, 0, 271, 241))
        self.frame_controls.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_controls.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_controls.setObjectName(_fromUtf8("frame_controls"))
        self.bar_right = QtGui.QProgressBar(self.frame_controls)
        self.bar_right.setGeometry(QtCore.QRect(160, 200, 91, 31))
        self.bar_right.setProperty("value", 0)
        self.bar_right.setTextVisible(False)
        self.bar_right.setOrientation(QtCore.Qt.Horizontal)
        self.bar_right.setInvertedAppearance(False)
        self.bar_right.setObjectName(_fromUtf8("bar_right"))
        self.btn_reverse = QtGui.QPushButton(self.frame_controls)
        self.btn_reverse.setGeometry(QtCore.QRect(140, 140, 41, 41))
        self.btn_reverse.setObjectName(_fromUtf8("btn_reverse"))
        self.btn_stop = QtGui.QPushButton(self.frame_controls)
        self.btn_stop.setGeometry(QtCore.QRect(120, 80, 85, 41))
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        self.btn_forward = QtGui.QPushButton(self.frame_controls)
        self.btn_forward.setGeometry(QtCore.QRect(140, 20, 41, 41))
        self.btn_forward.setObjectName(_fromUtf8("btn_forward"))
        self.bar_forward = QtGui.QProgressBar(self.frame_controls)
        self.bar_forward.setGeometry(QtCore.QRect(10, 10, 31, 91))
        self.bar_forward.setProperty("value", 0)
        self.bar_forward.setTextVisible(False)
        self.bar_forward.setOrientation(QtCore.Qt.Vertical)
        self.bar_forward.setInvertedAppearance(False)
        self.bar_forward.setObjectName(_fromUtf8("bar_forward"))
        self.bar_left = QtGui.QProgressBar(self.frame_controls)
        self.bar_left.setGeometry(QtCore.QRect(70, 200, 91, 31))
        self.bar_left.setProperty("value", 0)
        self.bar_left.setOrientation(QtCore.Qt.Horizontal)
        self.bar_left.setInvertedAppearance(True)
        self.bar_left.setFormat(_fromUtf8(""))
        self.bar_left.setObjectName(_fromUtf8("bar_left"))
        self.btn_left = QtGui.QPushButton(self.frame_controls)
        self.btn_left.setGeometry(QtCore.QRect(60, 80, 41, 41))
        self.btn_left.setObjectName(_fromUtf8("btn_left"))
        self.btn_right = QtGui.QPushButton(self.frame_controls)
        self.btn_right.setGeometry(QtCore.QRect(220, 80, 41, 41))
        self.btn_right.setObjectName(_fromUtf8("btn_right"))
        self.bar_reverse = QtGui.QProgressBar(self.frame_controls)
        self.bar_reverse.setGeometry(QtCore.QRect(10, 100, 31, 91))
        self.bar_reverse.setProperty("value", 0)
        self.bar_reverse.setOrientation(QtCore.Qt.Vertical)
        self.bar_reverse.setInvertedAppearance(True)
        self.bar_reverse.setFormat(_fromUtf8(""))
        self.bar_reverse.setObjectName(_fromUtf8("bar_reverse"))
        self.lbl_brake = QtGui.QLabel(self.frame_controls)
        self.lbl_brake.setGeometry(QtCore.QRect(15, 216, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_brake.setFont(font)
        self.lbl_brake.setObjectName(_fromUtf8("lbl_brake"))
        self.rb_brake = QtGui.QRadioButton(self.frame_controls)
        self.rb_brake.setGeometry(QtCore.QRect(15, 200, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.rb_brake.setFont(font)
        self.rb_brake.setText(_fromUtf8(""))
        self.rb_brake.setIconSize(QtCore.QSize(20, 20))
        self.rb_brake.setCheckable(True)
        self.rb_brake.setObjectName(_fromUtf8("rb_brake"))
        self.btn_left_full = QtGui.QPushButton(self.frame_controls)
        self.btn_left_full.setGeometry(QtCore.QRect(60, 120, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.btn_left_full.setFont(font)
        self.btn_left_full.setObjectName(_fromUtf8("btn_left_full"))
        self.btn_right_full = QtGui.QPushButton(self.frame_controls)
        self.btn_right_full.setGeometry(QtCore.QRect(220, 120, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.btn_right_full.setFont(font)
        self.btn_right_full.setObjectName(_fromUtf8("btn_right_full"))
        self.frame_data = QtGui.QFrame(self.centralwidget)
        self.frame_data.setGeometry(QtCore.QRect(0, 250, 551, 191))
        self.frame_data.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_data.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_data.setObjectName(_fromUtf8("frame_data"))
        self.tab_sensors = QtGui.QTabWidget(self.frame_data)
        self.tab_sensors.setGeometry(QtCore.QRect(300, 10, 241, 171))
        self.tab_sensors.setObjectName(_fromUtf8("tab_sensors"))
        self.tab_environment = QtGui.QWidget()
        self.tab_environment.setObjectName(_fromUtf8("tab_environment"))
        self.tb_temperature = QtGui.QLineEdit(self.tab_environment)
        self.tb_temperature.setGeometry(QtCore.QRect(90, 30, 91, 25))
        self.tb_temperature.setText(_fromUtf8(""))
        self.tb_temperature.setPlaceholderText(_fromUtf8(""))
        self.tb_temperature.setObjectName(_fromUtf8("tb_temperature"))
        self.lbl_temperature = QtGui.QLabel(self.tab_environment)
        self.lbl_temperature.setGeometry(QtCore.QRect(13, 32, 70, 21))
        self.lbl_temperature.setObjectName(_fromUtf8("lbl_temperature"))
        self.lbl_humidity = QtGui.QLabel(self.tab_environment)
        self.lbl_humidity.setGeometry(QtCore.QRect(28, 62, 54, 21))
        self.lbl_humidity.setObjectName(_fromUtf8("lbl_humidity"))
        self.tb_humidity = QtGui.QLineEdit(self.tab_environment)
        self.tb_humidity.setGeometry(QtCore.QRect(90, 60, 91, 25))
        self.tb_humidity.setText(_fromUtf8(""))
        self.tb_humidity.setPlaceholderText(_fromUtf8(""))
        self.tb_humidity.setObjectName(_fromUtf8("tb_humidity"))
        self.tb_pressure = QtGui.QLineEdit(self.tab_environment)
        self.tb_pressure.setGeometry(QtCore.QRect(90, 90, 91, 25))
        self.tb_pressure.setText(_fromUtf8(""))
        self.tb_pressure.setPlaceholderText(_fromUtf8(""))
        self.tb_pressure.setObjectName(_fromUtf8("tb_pressure"))
        self.lbl_pressure = QtGui.QLabel(self.tab_environment)
        self.lbl_pressure.setGeometry(QtCore.QRect(30, 92, 54, 21))
        self.lbl_pressure.setObjectName(_fromUtf8("lbl_pressure"))
        self.tab_sensors.addTab(self.tab_environment, _fromUtf8(""))
        self.tab_gps = QtGui.QWidget()
        self.tab_gps.setObjectName(_fromUtf8("tab_gps"))
        self.tb_gps_north = QtGui.QLineEdit(self.tab_gps)
        self.tb_gps_north.setGeometry(QtCore.QRect(90, 16, 91, 25))
        self.tb_gps_north.setText(_fromUtf8(""))
        self.tb_gps_north.setPlaceholderText(_fromUtf8(""))
        self.tb_gps_north.setObjectName(_fromUtf8("tb_gps_north"))
        self.lbl_gps_north = QtGui.QLabel(self.tab_gps)
        self.lbl_gps_north.setGeometry(QtCore.QRect(30, 18, 54, 21))
        self.lbl_gps_north.setObjectName(_fromUtf8("lbl_gps_north"))
        self.tb_gps_east = QtGui.QLineEdit(self.tab_gps)
        self.tb_gps_east.setGeometry(QtCore.QRect(90, 46, 91, 25))
        self.tb_gps_east.setText(_fromUtf8(""))
        self.tb_gps_east.setPlaceholderText(_fromUtf8(""))
        self.tb_gps_east.setObjectName(_fromUtf8("tb_gps_east"))
        self.lbl_gps_east = QtGui.QLabel(self.tab_gps)
        self.lbl_gps_east.setGeometry(QtCore.QRect(30, 48, 54, 21))
        self.lbl_gps_east.setObjectName(_fromUtf8("lbl_gps_east"))
        self.tb_gps_speed = QtGui.QLineEdit(self.tab_gps)
        self.tb_gps_speed.setGeometry(QtCore.QRect(90, 76, 91, 25))
        self.tb_gps_speed.setText(_fromUtf8(""))
        self.tb_gps_speed.setPlaceholderText(_fromUtf8(""))
        self.tb_gps_speed.setObjectName(_fromUtf8("tb_gps_speed"))
        self.lbl_gps_speed = QtGui.QLabel(self.tab_gps)
        self.lbl_gps_speed.setGeometry(QtCore.QRect(30, 78, 54, 21))
        self.lbl_gps_speed.setObjectName(_fromUtf8("lbl_gps_speed"))
        self.lbl_gps_altitude = QtGui.QLabel(self.tab_gps)
        self.lbl_gps_altitude.setGeometry(QtCore.QRect(30, 110, 54, 21))
        self.lbl_gps_altitude.setObjectName(_fromUtf8("lbl_gps_altitude"))
        self.tb_gps_altitude = QtGui.QLineEdit(self.tab_gps)
        self.tb_gps_altitude.setGeometry(QtCore.QRect(90, 108, 91, 25))
        self.tb_gps_altitude.setText(_fromUtf8(""))
        self.tb_gps_altitude.setPlaceholderText(_fromUtf8(""))
        self.tb_gps_altitude.setObjectName(_fromUtf8("tb_gps_altitude"))
        self.tab_sensors.addTab(self.tab_gps, _fromUtf8(""))
        self.tab_compass = QtGui.QWidget()
        self.tab_compass.setObjectName(_fromUtf8("tab_compass"))
        self.tab_sensors.addTab(self.tab_compass, _fromUtf8(""))
        self.tab_gyro = QtGui.QWidget()
        self.tab_gyro.setObjectName(_fromUtf8("tab_gyro"))
        self.tab_sensors.addTab(self.tab_gyro, _fromUtf8(""))
        self.lbl_battery_a_2 = QtGui.QLabel(self.frame_data)
        self.lbl_battery_a_2.setGeometry(QtCore.QRect(160, 120, 71, 21))
        self.lbl_battery_a_2.setObjectName(_fromUtf8("lbl_battery_a_2"))
        self.bar_battery_a = QtGui.QProgressBar(self.frame_data)
        self.bar_battery_a.setGeometry(QtCore.QRect(40, 80, 118, 23))
        self.bar_battery_a.setProperty("value", 0)
        self.bar_battery_a.setObjectName(_fromUtf8("bar_battery_a"))
        self.bar_battery_b = QtGui.QProgressBar(self.frame_data)
        self.bar_battery_b.setGeometry(QtCore.QRect(40, 120, 118, 23))
        self.bar_battery_b.setProperty("value", 0)
        self.bar_battery_b.setObjectName(_fromUtf8("bar_battery_b"))
        self.lbl_battery_a = QtGui.QLabel(self.frame_data)
        self.lbl_battery_a.setGeometry(QtCore.QRect(160, 80, 71, 21))
        self.lbl_battery_a.setObjectName(_fromUtf8("lbl_battery_a"))
        self.lbl_wifi = QtGui.QLabel(self.frame_data)
        self.lbl_wifi.setGeometry(QtCore.QRect(160, 40, 54, 21))
        self.lbl_wifi.setObjectName(_fromUtf8("lbl_wifi"))
        self.bar_wifi = QtGui.QProgressBar(self.frame_data)
        self.bar_wifi.setGeometry(QtCore.QRect(40, 40, 118, 23))
        self.bar_wifi.setProperty("value", 0)
        self.bar_wifi.setObjectName(_fromUtf8("bar_wifi"))
        self.frame_camera = QtGui.QFrame(self.centralwidget)
        self.frame_camera.setGeometry(QtCore.QRect(280, 0, 271, 241))
        self.frame_camera.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_camera.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_camera.setObjectName(_fromUtf8("frame_camera"))
        self.dial_cam_pan = QtGui.QDial(self.frame_camera)
        self.dial_cam_pan.setGeometry(QtCore.QRect(110, 80, 91, 91))
        self.dial_cam_pan.setMaximum(100)
        self.dial_cam_pan.setProperty("value", 50)
        self.dial_cam_pan.setWrapping(True)
        self.dial_cam_pan.setNotchTarget(12.5)
        self.dial_cam_pan.setNotchesVisible(True)
        self.dial_cam_pan.setObjectName(_fromUtf8("dial_cam_pan"))
        self.slider_cam_tilt = QtGui.QSlider(self.frame_camera)
        self.slider_cam_tilt.setGeometry(QtCore.QRect(50, 40, 29, 160))
        self.slider_cam_tilt.setMaximum(100)
        self.slider_cam_tilt.setProperty("value", 50)
        self.slider_cam_tilt.setSliderPosition(50)
        self.slider_cam_tilt.setTracking(True)
        self.slider_cam_tilt.setOrientation(QtCore.Qt.Vertical)
        self.slider_cam_tilt.setInvertedAppearance(False)
        self.slider_cam_tilt.setTickPosition(QtGui.QSlider.TicksAbove)
        self.slider_cam_tilt.setTickInterval(10)
        self.slider_cam_tilt.setObjectName(_fromUtf8("slider_cam_tilt"))
        self.lbl_cam_dial = QtGui.QLabel(self.frame_camera)
        self.lbl_cam_dial.setGeometry(QtCore.QRect(146, 65, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_cam_dial.setFont(font)
        self.lbl_cam_dial.setObjectName(_fromUtf8("lbl_cam_dial"))
        self.lbl_cam_tilt = QtGui.QLabel(self.frame_camera)
        self.lbl_cam_tilt.setGeometry(QtCore.QRect(70, 180, 31, 16))
        self.lbl_cam_tilt.setObjectName(_fromUtf8("lbl_cam_tilt"))
        self.lbl_cam_pan = QtGui.QLabel(self.frame_camera)
        self.lbl_cam_pan.setGeometry(QtCore.QRect(170, 160, 31, 16))
        self.lbl_cam_pan.setObjectName(_fromUtf8("lbl_cam_pan"))
        self.btn_cam_reset = QtGui.QToolButton(self.frame_camera)
        self.btn_cam_reset.setGeometry(QtCore.QRect(210, 200, 41, 23))
        self.btn_cam_reset.setObjectName(_fromUtf8("btn_cam_reset"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_sensors.setCurrentIndex(0)
        QtCore.QObject.connect(self.btn_forward, QtCore.SIGNAL(_fromUtf8("clicked()")), self.increment_throttle)
        QtCore.QObject.connect(self.btn_reverse, QtCore.SIGNAL(_fromUtf8("clicked()")), self.decrement_throttle)
        QtCore.QObject.connect(self.btn_stop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.all_stop)
        QtCore.QObject.connect(self.rb_brake, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_brake)
        QtCore.QObject.connect(self.btn_left, QtCore.SIGNAL(_fromUtf8("clicked()")), self.decrement_direction)
        QtCore.QObject.connect(self.btn_right, QtCore.SIGNAL(_fromUtf8("clicked()")), self.increment_direction)
        QtCore.QObject.connect(self.btn_left_full, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_zero_direction)
        QtCore.QObject.connect(self.btn_right_full, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_full_direction)
        QtCore.QObject.connect(self.btn_cam_reset, QtCore.SIGNAL(_fromUtf8("clicked()")), self.reset_camera)
        QtCore.QObject.connect(self.slider_cam_tilt, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), self.tilt_camera)
        QtCore.QObject.connect(self.dial_cam_pan, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), self.pan_camera)
        QtCore.QObject.connect(self.slider_cam_tilt, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.tilt_camera)
        QtCore.QObject.connect(self.dial_cam_pan, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.pan_camera)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Pi Rover", None))
        self.bar_right.setFormat(_translate("MainWindow", "%p%", None))
        self.btn_reverse.setText(_translate("MainWindow", "REV", None))
        self.btn_stop.setText(_translate("MainWindow", "STOP", None))
        self.btn_forward.setText(_translate("MainWindow", "FWD", None))
        self.bar_forward.setFormat(_translate("MainWindow", "%p%", None))
        self.btn_left.setText(_translate("MainWindow", "LEFT", None))
        self.btn_right.setText(_translate("MainWindow", "RGHT", None))
        self.lbl_brake.setText(_translate("MainWindow", "brake", None))
        self.btn_left_full.setText(_translate("MainWindow", "full", None))
        self.btn_right_full.setText(_translate("MainWindow", "full", None))
        self.lbl_temperature.setText(_translate("MainWindow", "Temperture", None))
        self.lbl_humidity.setText(_translate("MainWindow", "Humidity", None))
        self.lbl_pressure.setText(_translate("MainWindow", "Pressure", None))
        self.tab_sensors.setTabText(self.tab_sensors.indexOf(self.tab_environment), _translate("MainWindow", "Environment", None))
        self.lbl_gps_north.setText(_translate("MainWindow", "North", None))
        self.lbl_gps_east.setText(_translate("MainWindow", "East", None))
        self.lbl_gps_speed.setText(_translate("MainWindow", "Speed", None))
        self.lbl_gps_altitude.setText(_translate("MainWindow", "Altitude", None))
        self.tab_sensors.setTabText(self.tab_sensors.indexOf(self.tab_gps), _translate("MainWindow", "GPS", None))
        self.tab_sensors.setTabText(self.tab_sensors.indexOf(self.tab_compass), _translate("MainWindow", "Compass", None))
        self.tab_sensors.setTabText(self.tab_sensors.indexOf(self.tab_gyro), _translate("MainWindow", "Gyro", None))
        self.lbl_battery_a_2.setText(_translate("MainWindow", "Battery - B", None))
        self.lbl_battery_a.setText(_translate("MainWindow", "Battery - A", None))
        self.lbl_wifi.setText(_translate("MainWindow", "Wifi", None))
        self.bar_wifi.setFormat(_translate("MainWindow", "%p%", None))
        self.lbl_cam_dial.setText(_translate("MainWindow", "front", None))
        self.lbl_cam_tilt.setText(_translate("MainWindow", "Tilt", None))
        self.lbl_cam_pan.setText(_translate("MainWindow", "Pan", None))
        self.btn_cam_reset.setText(_translate("MainWindow", "RESET", None))

        # Create QThreads for MQ transactions
        # MQ Reader
        self.MQReadThread = workers.MQReader(queue='test_q', mqhost='localhost')
        MainWindow.connect(self.MQReadThread, self.MQReadThread.signal, self.translateQueueData)
        self.MQReadThread.start()


    def translateQueueData(self, queue_data):
        json_data = json.loads(queue_data)

        if 'environment' in json_data:
            if 'temperature' in json_data['environment']: self.tb_temperature.setText(str(json_data['environment']['temperature']))
            if 'humidity' in json_data['environment']: self.tb_humidity.setText(str(json_data['environment']['humidity']))


    def increment_throttle(self):
        forward_value = self.bar_forward.value()
        reverse_value = self.bar_reverse.value()

        if reverse_value == 0:
             if forward_value < 100: 
                 self.bar_forward.setValue(forward_value + 10)
                 self.rb_brake.setChecked(False)
        else:
             self.bar_reverse.setValue(reverse_value - 10)

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')


    def decrement_throttle(self):
        forward_value = self.bar_forward.value()
        reverse_value = self.bar_reverse.value()

        if forward_value == 0:
             if reverse_value < 100: 
                self.bar_reverse.setValue(reverse_value + 10)
                self.rb_brake.setChecked(False)
        else:
             self.bar_forward.setValue(forward_value - 10)

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')



    def all_stop(self):
        forward_value = self.bar_forward.value()
        reverse_value = self.bar_reverse.value()
        right_value = self.bar_right.value()
        left_value = self.bar_left.value()


        if forward_value > 0 or reverse_value > 0 or left_value > 0 or right_value > 0: 
            self.bar_forward.setValue(0)
            self.bar_reverse.setValue(0)
            self.bar_left.setValue(0)
            self.bar_right.setValue(0)
            self.rb_brake.setChecked(True)
        else:
            self.rb_brake.toggle()

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')


    def set_brake(self):
        brake_value = self.rb_brake.isChecked()

        if brake_value == True:
            self.bar_forward.setValue(0)
            self.bar_reverse.setValue(0)
        
        workers.MQWriter(self, queue='test_qw', mqhost='localhost')

        
    def increment_direction(self):
        right_value = self.bar_right.value()
        left_value = self.bar_left.value()

        if left_value == 0:
             if right_value < 100: self.bar_right.setValue(right_value + 10)
        else:
             self.bar_left.setValue(left_value - 10)

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')


    def decrement_direction(self):
        right_value = self.bar_right.value()
        left_value = self.bar_left.value()

        if right_value == 0:
             if left_value < 100: self.bar_left.setValue(left_value + 10)
        else:
             self.bar_right.setValue(right_value - 10)

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')


    def set_full_direction(self):
        right_value = self.bar_right.value()

        if right_value < 100:
             self.bar_right.setValue(100)
             self.bar_left.setValue(0)
        else:
             self.bar_right.setValue(0)

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')



    def set_zero_direction(self):
        left_value = self.bar_left.value()

        if left_value < 100:
             self.bar_left.setValue(100)
             self.bar_right.setValue(0)
        else:
             self.bar_left.setValue(0)

        workers.MQWriter(self, queue='test_qw', mqhost='localhost')

            
    def reset_camera(self):
        self.dial_cam_pan.setValue(50)                        
        self.slider_cam_tilt.setValue(50)                        
        workers.MQWriter(self, queue='test_qw', mqhost='localhost')
            

    def tilt_camera(self):
        workers.MQWriter(self, queue='test_qw', mqhost='localhost')

    def pan_camera(self):
        workers.MQWriter(self, queue='test_qw', mqhost='localhost')
