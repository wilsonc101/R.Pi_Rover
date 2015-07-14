# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rover_monitor.ui'
#
# Created: Thu Jan  1 15:55:44 2015
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
        MainWindow.resize(493, 462)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame_controls = QtGui.QFrame(self.centralwidget)
        self.frame_controls.setGeometry(QtCore.QRect(10, 150, 331, 131))
        self.frame_controls.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_controls.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_controls.setObjectName(_fromUtf8("frame_controls"))
        self.label_rev = QtGui.QLabel(self.frame_controls)
        self.label_rev.setGeometry(QtCore.QRect(33, 34, 21, 20))
        self.label_rev.setObjectName(_fromUtf8("label_rev"))
        self.label = QtGui.QLabel(self.frame_controls)
        self.label.setGeometry(QtCore.QRect(132, 20, 54, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_direction = QtGui.QLabel(self.frame_controls)
        self.label_direction.setGeometry(QtCore.QRect(129, 60, 54, 15))
        self.label_direction.setObjectName(_fromUtf8("label_direction"))
        self.label_forward = QtGui.QLabel(self.frame_controls)
        self.label_forward.setGeometry(QtCore.QRect(260, 34, 54, 20))
        self.label_forward.setObjectName(_fromUtf8("label_forward"))
        self.label_left = QtGui.QLabel(self.frame_controls)
        self.label_left.setGeometry(QtCore.QRect(32, 74, 31, 20))
        self.label_left.setObjectName(_fromUtf8("label_left"))
        self.label_right = QtGui.QLabel(self.frame_controls)
        self.label_right.setGeometry(QtCore.QRect(259, 74, 41, 20))
        self.label_right.setObjectName(_fromUtf8("label_right"))
        self.lbl_control = QtGui.QLabel(self.frame_controls)
        self.lbl_control.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_control.setFont(font)
        self.lbl_control.setObjectName(_fromUtf8("lbl_control"))
        self.slider_throttle = QtGui.QSlider(self.frame_controls)
        self.slider_throttle.setGeometry(QtCore.QRect(60, 30, 191, 29))
        self.slider_throttle.setMinimum(-100)
        self.slider_throttle.setMaximum(100)
        self.slider_throttle.setTracking(True)
        self.slider_throttle.setOrientation(QtCore.Qt.Horizontal)
        self.slider_throttle.setTickPosition(QtGui.QSlider.NoTicks)
        self.slider_throttle.setObjectName(_fromUtf8("slider_throttle"))
        self.slider_direction = QtGui.QSlider(self.frame_controls)
        self.slider_direction.setGeometry(QtCore.QRect(60, 70, 191, 29))
        self.slider_direction.setMinimum(-100)
        self.slider_direction.setMaximum(100)
        self.slider_direction.setTracking(True)
        self.slider_direction.setOrientation(QtCore.Qt.Horizontal)
        self.slider_direction.setTickPosition(QtGui.QSlider.NoTicks)
        self.slider_direction.setObjectName(_fromUtf8("slider_direction"))
        self.rb_brake = QtGui.QRadioButton(self.frame_controls)
        self.rb_brake.setGeometry(QtCore.QRect(30, 100, 100, 21))
        self.rb_brake.setObjectName(_fromUtf8("rb_brake"))
        self.frame_gps = QtGui.QFrame(self.centralwidget)
        self.frame_gps.setGeometry(QtCore.QRect(350, 290, 131, 141))
        self.frame_gps.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_gps.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_gps.setObjectName(_fromUtf8("frame_gps"))
        self.lbl_altitude = QtGui.QLabel(self.frame_gps)
        self.lbl_altitude.setGeometry(QtCore.QRect(10, 100, 51, 20))
        self.lbl_altitude.setObjectName(_fromUtf8("lbl_altitude"))
        self.lbl_east = QtGui.QLabel(self.frame_gps)
        self.lbl_east.setGeometry(QtCore.QRect(31, 46, 31, 20))
        self.lbl_east.setObjectName(_fromUtf8("lbl_east"))
        self.lbl_speed = QtGui.QLabel(self.frame_gps)
        self.lbl_speed.setGeometry(QtCore.QRect(21, 73, 41, 20))
        self.lbl_speed.setObjectName(_fromUtf8("lbl_speed"))
        self.lbl_north = QtGui.QLabel(self.frame_gps)
        self.lbl_north.setGeometry(QtCore.QRect(23, 19, 41, 20))
        self.lbl_north.setObjectName(_fromUtf8("lbl_north"))
        self.lbl_gps = QtGui.QLabel(self.frame_gps)
        self.lbl_gps.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_gps.setFont(font)
        self.lbl_gps.setObjectName(_fromUtf8("lbl_gps"))
        self.tb_north = QtGui.QLineEdit(self.frame_gps)
        self.tb_north.setGeometry(QtCore.QRect(60, 17, 51, 25))
        self.tb_north.setObjectName(_fromUtf8("tb_north"))
        self.tb_east = QtGui.QLineEdit(self.frame_gps)
        self.tb_east.setGeometry(QtCore.QRect(60, 44, 51, 25))
        self.tb_east.setObjectName(_fromUtf8("tb_east"))
        self.tb_speed = QtGui.QLineEdit(self.frame_gps)
        self.tb_speed.setGeometry(QtCore.QRect(60, 71, 51, 25))
        self.tb_speed.setObjectName(_fromUtf8("tb_speed"))
        self.tb_altitude = QtGui.QLineEdit(self.frame_gps)
        self.tb_altitude.setGeometry(QtCore.QRect(60, 98, 51, 25))
        self.tb_altitude.setObjectName(_fromUtf8("tb_altitude"))
        self.frame_environment = QtGui.QFrame(self.centralwidget)
        self.frame_environment.setGeometry(QtCore.QRect(170, 290, 161, 141))
        self.frame_environment.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_environment.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_environment.setObjectName(_fromUtf8("frame_environment"))
        self.lbl_pressure = QtGui.QLabel(self.frame_environment)
        self.lbl_pressure.setGeometry(QtCore.QRect(37, 90, 51, 20))
        self.lbl_pressure.setObjectName(_fromUtf8("lbl_pressure"))
        self.lbl_humidity = QtGui.QLabel(self.frame_environment)
        self.lbl_humidity.setGeometry(QtCore.QRect(35, 63, 51, 20))
        self.lbl_humidity.setObjectName(_fromUtf8("lbl_humidity"))
        self.lbl_temperature = QtGui.QLabel(self.frame_environment)
        self.lbl_temperature.setGeometry(QtCore.QRect(14, 36, 71, 20))
        self.lbl_temperature.setObjectName(_fromUtf8("lbl_temperature"))
        self.lbl_environment = QtGui.QLabel(self.frame_environment)
        self.lbl_environment.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_environment.setFont(font)
        self.lbl_environment.setObjectName(_fromUtf8("lbl_environment"))
        self.tb_temperature = QtGui.QLineEdit(self.frame_environment)
        self.tb_temperature.setGeometry(QtCore.QRect(90, 34, 51, 25))
        self.tb_temperature.setObjectName(_fromUtf8("tb_temperature"))
        self.tb_humidity = QtGui.QLineEdit(self.frame_environment)
        self.tb_humidity.setGeometry(QtCore.QRect(90, 61, 51, 25))
        self.tb_humidity.setObjectName(_fromUtf8("tb_humidity"))
        self.tb_pressure = QtGui.QLineEdit(self.frame_environment)
        self.tb_pressure.setGeometry(QtCore.QRect(90, 88, 51, 25))
        self.tb_pressure.setObjectName(_fromUtf8("tb_pressure"))
        self.frame_vehicle = QtGui.QFrame(self.centralwidget)
        self.frame_vehicle.setGeometry(QtCore.QRect(10, 290, 141, 141))
        self.frame_vehicle.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_vehicle.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_vehicle.setObjectName(_fromUtf8("frame_vehicle"))
        self.lbl_wifi = QtGui.QLabel(self.frame_vehicle)
        self.lbl_wifi.setGeometry(QtCore.QRect(42, 33, 31, 20))
        self.lbl_wifi.setObjectName(_fromUtf8("lbl_wifi"))
        self.lbl_vehicle = QtGui.QLabel(self.frame_vehicle)
        self.lbl_vehicle.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_vehicle.setFont(font)
        self.lbl_vehicle.setObjectName(_fromUtf8("lbl_vehicle"))
        self.lbl_batt_a = QtGui.QLabel(self.frame_vehicle)
        self.lbl_batt_a.setGeometry(QtCore.QRect(26, 60, 51, 20))
        self.lbl_batt_a.setObjectName(_fromUtf8("lbl_batt_a"))
        self.lbl_batt_b = QtGui.QLabel(self.frame_vehicle)
        self.lbl_batt_b.setGeometry(QtCore.QRect(26, 88, 51, 20))
        self.lbl_batt_b.setObjectName(_fromUtf8("lbl_batt_b"))
        self.tb_wifi = QtGui.QLineEdit(self.frame_vehicle)
        self.tb_wifi.setGeometry(QtCore.QRect(70, 30, 51, 25))
        self.tb_wifi.setObjectName(_fromUtf8("tb_wifi"))
        self.tb_batt_a = QtGui.QLineEdit(self.frame_vehicle)
        self.tb_batt_a.setGeometry(QtCore.QRect(70, 57, 51, 25))
        self.tb_batt_a.setObjectName(_fromUtf8("tb_batt_a"))
        self.tb_batt_b = QtGui.QLineEdit(self.frame_vehicle)
        self.tb_batt_b.setGeometry(QtCore.QRect(70, 84, 51, 25))
        self.tb_batt_b.setObjectName(_fromUtf8("tb_batt_b"))
        self.frame_camera = QtGui.QFrame(self.centralwidget)
        self.frame_camera.setGeometry(QtCore.QRect(360, 150, 121, 131))
        self.frame_camera.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_camera.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_camera.setObjectName(_fromUtf8("frame_camera"))
        self.slider_cam_tilt = QtGui.QSlider(self.frame_camera)
        self.slider_cam_tilt.setGeometry(QtCore.QRect(10, 20, 29, 91))
        self.slider_cam_tilt.setMinimum(-100)
        self.slider_cam_tilt.setMaximum(100)
        self.slider_cam_tilt.setOrientation(QtCore.Qt.Vertical)
        self.slider_cam_tilt.setObjectName(_fromUtf8("slider_cam_tilt"))
        self.dial_cam_pan = QtGui.QDial(self.frame_camera)
        self.dial_cam_pan.setGeometry(QtCore.QRect(50, 30, 61, 71))
        self.dial_cam_pan.setMinimum(-100)
        self.dial_cam_pan.setMaximum(100)
        self.dial_cam_pan.setObjectName(_fromUtf8("dial_cam_pan"))
        self.label_tilt = QtGui.QLabel(self.frame_camera)
        self.label_tilt.setGeometry(QtCore.QRect(34, 100, 21, 16))
        self.label_tilt.setObjectName(_fromUtf8("label_tilt"))
        self.label_pan = QtGui.QLabel(self.frame_camera)
        self.label_pan.setGeometry(QtCore.QRect(93, 26, 21, 16))
        self.label_pan.setObjectName(_fromUtf8("label_pan"))
        self.lbl_camera = QtGui.QLabel(self.frame_camera)
        self.lbl_camera.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_camera.setFont(font)
        self.lbl_camera.setObjectName(_fromUtf8("lbl_camera"))
        self.frame_queues = QtGui.QFrame(self.centralwidget)
        self.frame_queues.setGeometry(QtCore.QRect(10, 10, 471, 131))
        self.frame_queues.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_queues.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_queues.setObjectName(_fromUtf8("frame_queues"))
        self.btn_subscribe = QtGui.QPushButton(self.frame_queues)
        self.btn_subscribe.setGeometry(QtCore.QRect(390, 20, 71, 27))
        self.btn_subscribe.setObjectName(_fromUtf8("btn_subscribe"))
        self.lbl_queues = QtGui.QLabel(self.frame_queues)
        self.lbl_queues.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_queues.setFont(font)
        self.lbl_queues.setObjectName(_fromUtf8("lbl_queues"))
        self.frame_control = QtGui.QFrame(self.frame_queues)
        self.frame_control.setGeometry(QtCore.QRect(10, 20, 181, 101))
        self.frame_control.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_control.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_control.setObjectName(_fromUtf8("frame_control"))
        self.lbl_control_name = QtGui.QLabel(self.frame_control)
        self.lbl_control_name.setGeometry(QtCore.QRect(12, 25, 41, 16))
        self.lbl_control_name.setObjectName(_fromUtf8("lbl_control_name"))
        self.tb_control_server = QtGui.QLineEdit(self.frame_control)
        self.tb_control_server.setGeometry(QtCore.QRect(60, 55, 113, 25))
        self.tb_control_server.setObjectName(_fromUtf8("tb_control_server"))
        self.tb_control_name = QtGui.QLineEdit(self.frame_control)
        self.tb_control_name.setGeometry(QtCore.QRect(60, 20, 113, 25))
        self.tb_control_name.setObjectName(_fromUtf8("tb_control_name"))
        self.lbl_control_server = QtGui.QLabel(self.frame_control)
        self.lbl_control_server.setGeometry(QtCore.QRect(12, 60, 41, 16))
        self.lbl_control_server.setObjectName(_fromUtf8("lbl_control_server"))
        self.lbl_queue_control = QtGui.QLabel(self.frame_control)
        self.lbl_queue_control.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_queue_control.setFont(font)
        self.lbl_queue_control.setObjectName(_fromUtf8("lbl_queue_control"))
        self.frame_vehicle_2 = QtGui.QFrame(self.frame_queues)
        self.frame_vehicle_2.setGeometry(QtCore.QRect(200, 20, 181, 101))
        self.frame_vehicle_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_vehicle_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_vehicle_2.setObjectName(_fromUtf8("frame_vehicle_2"))
        self.lbl_queue_vehicle = QtGui.QLabel(self.frame_vehicle_2)
        self.lbl_queue_vehicle.setGeometry(QtCore.QRect(3, 3, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_queue_vehicle.setFont(font)
        self.lbl_queue_vehicle.setObjectName(_fromUtf8("lbl_queue_vehicle"))
        self.lbl_vehicle_server = QtGui.QLabel(self.frame_vehicle_2)
        self.lbl_vehicle_server.setGeometry(QtCore.QRect(14, 65, 41, 16))
        self.lbl_vehicle_server.setObjectName(_fromUtf8("lbl_vehicle_server"))
        self.lbl_vehicle_name = QtGui.QLabel(self.frame_vehicle_2)
        self.lbl_vehicle_name.setGeometry(QtCore.QRect(14, 30, 41, 16))
        self.lbl_vehicle_name.setObjectName(_fromUtf8("lbl_vehicle_name"))
        self.tb_vehicle_name = QtGui.QLineEdit(self.frame_vehicle_2)
        self.tb_vehicle_name.setGeometry(QtCore.QRect(60, 25, 113, 25))
        self.tb_vehicle_name.setObjectName(_fromUtf8("tb_vehicle_name"))
        self.tb_vehicle_server = QtGui.QLineEdit(self.frame_vehicle_2)
        self.tb_vehicle_server.setGeometry(QtCore.QRect(60, 60, 113, 25))
        self.tb_vehicle_server.setObjectName(_fromUtf8("tb_vehicle_server"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.btn_subscribe, QtCore.SIGNAL(_fromUtf8("clicked()")), self.queue_subscribe)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Rover Monitor", None))
        self.label_rev.setText(_translate("MainWindow", "Rev", None))
        self.label.setText(_translate("MainWindow", "Throttle", None))
        self.label_direction.setText(_translate("MainWindow", "Direction", None))
        self.label_forward.setText(_translate("MainWindow", "Forward", None))
        self.label_left.setText(_translate("MainWindow", "Left", None))
        self.label_right.setText(_translate("MainWindow", "Right", None))
        self.lbl_control.setText(_translate("MainWindow", "Controls", None))
        self.rb_brake.setText(_translate("MainWindow", "Brake", None))
        self.lbl_altitude.setText(_translate("MainWindow", "Altitude", None))
        self.lbl_east.setText(_translate("MainWindow", "East", None))
        self.lbl_speed.setText(_translate("MainWindow", "Speed", None))
        self.lbl_north.setText(_translate("MainWindow", "North", None))
        self.lbl_gps.setText(_translate("MainWindow", "GPS", None))
        self.lbl_pressure.setText(_translate("MainWindow", "Pressure", None))
        self.lbl_humidity.setText(_translate("MainWindow", "Humidity", None))
        self.lbl_temperature.setText(_translate("MainWindow", "Temperature", None))
        self.lbl_environment.setText(_translate("MainWindow", "Environment", None))
        self.lbl_wifi.setText(_translate("MainWindow", "Wifi", None))
        self.lbl_vehicle.setText(_translate("MainWindow", "Vehicle", None))
        self.lbl_batt_a.setText(_translate("MainWindow", "Batt - A", None))
        self.lbl_batt_b.setText(_translate("MainWindow", "Batt - B", None))
        self.label_tilt.setText(_translate("MainWindow", "Tilt", None))
        self.label_pan.setText(_translate("MainWindow", "Pan", None))
        self.lbl_camera.setText(_translate("MainWindow", "Camera", None))
        self.btn_subscribe.setText(_translate("MainWindow", "Subscribe", None))
        self.lbl_queues.setText(_translate("MainWindow", "Data queues", None))
        self.lbl_control_name.setText(_translate("MainWindow", "Name", None))
        self.lbl_control_server.setText(_translate("MainWindow", "Server", None))
        self.lbl_queue_control.setText(_translate("MainWindow", "Control", None))
        self.lbl_queue_vehicle.setText(_translate("MainWindow", "Vehicle", None))
        self.lbl_vehicle_server.setText(_translate("MainWindow", "Server", None))
        self.lbl_vehicle_name.setText(_translate("MainWindow", "Name", None))


    def queue_subscribe(self):
        control_queue_name = str(self.tb_control_name.text())
        control_queue_server = str(self.tb_control_server.text())

        vehicle_queue_name = str(self.tb_vehicle_name.text())
        vehicle_queue_server = str(self.tb_vehicle_server.text())

        # Create QThreads for MQ transactions
        # MQ Reader - Control
        try:
            self.MQReadControl.terminate()
        except:
            print "Starting QT thread..."

        self.MQReadControl = workers.MQReader(control_queue_name, control_queue_server)
        QtCore.QObject.connect(self.MQReadControl, self.MQReadControl.signal, self.translateQueueData)
        self.MQReadControl.start()

        # MQ Reader - Vehicle
        try:
            self.MQReadVehicle.terminate()
        except:
            print "Starting QT thread..."

        self.MQReadVehicle = workers.MQReader(vehicle_queue_name, vehicle_queue_server)
        QtCore.QObject.connect(self.MQReadVehicle, self.MQReadVehicle.signal, self.translateQueueData)
        self.MQReadVehicle.start()


    def translateQueueData(self, queue_data):
        json_data = json.loads(queue_data)
        workers.GUIUpdate(self, json_data)


