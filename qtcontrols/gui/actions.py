import ConfigParser
from subprocess import Popen, PIPE


config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

CAMERA_SERVER = config.get('camera_server', 'server')
CAMERA_PORT = config.get('camera_server', 'port')



def GUIUpdate(qt_window, json_data):
    if 'vehicle' in json_data:
        if 'wifi' in json_data['vehicle']: qt_window.bar_wifi.setValue(int(json_data['vehicle']['wifi']))
        if 'batteryA' in json_data['vehicle']: qt_window.bar_battery_a.setValue(int(json_data['vehicle']['batteryA']))
        if 'batteryB' in json_data['vehicle']: qt_window.bar_battery_b.setValue(int(json_data['vehicle']['batteryB']))

    if 'environment' in json_data:
        if 'temperature' in json_data['environment']: qt_window.tb_temperature.setText(str(json_data['environment']['temperature']))
        if 'humidity' in json_data['environment']: qt_window.tb_humidity.setText(str(json_data['environment']['humidity']))
        if 'pressure' in json_data['environment']: qt_window.tb_pressure.setText(str(json_data['environment']['pressure']))

    if 'GPS' in json_data:
        if 'latitude' in json_data['GPS']: qt_window.tb_gps_lat.setText(str(json_data['GPS']['latitude']))
        if 'longitude' in json_data['GPS']: qt_window.tb_gps_long.setText(str(json_data['GPS']['longitude']))
        if 'speed' in json_data['GPS']: qt_window.tb_gps_speed.setText(str(json_data['GPS']['speed']))
        if 'altitude' in json_data['GPS']: qt_window.tb_gps_altitude.setText(str(json_data['GPS']['altitude']))

    if 'accelerometer' in json_data:
        if 'x' in json_data['accelerometer']:
            x_pos = int(json_data['accelerometer']['x'])
            rear = x_pos / 2
            front = (0 - x_pos) / 2
            qt_window.center_line_rf.setLine(-40, rear, 40, front)
            qt_window.wheel_re.setLine(-40, (rear-10), -40, (rear+10))
            qt_window.wheel_f.setLine(40, (front-10), 40, (front+10))

        if 'y' in json_data['accelerometer']:
            y_pos = int(json_data['accelerometer']['y'])
            left = (0 - y_pos) / 2
            right = y_pos / 2
            qt_window.center_line_lr.setLine(-40, left, 40, right)
            qt_window.wheel_l.setLine(-40, (left-10), -40, (left+10))
            qt_window.wheel_r.setLine(40, (right-10), 40, (right+10))
    
    if 'camera' in json_data:
        if 'still' in json_data['camera']:
            qt_window.lbl_cam_correl.setText(str(json_data['camera']['still']['correl']))


def OpenPlayer():
    cmd = "/bin/nc " + CAMERA_SERVER + " " + CAMERA_PORT + " | /usr/bin/mplayer -fps 60 -cache 2048 -really-quiet -"
    p = Popen(cmd, shell=True, stdout=PIPE)  
    return p
