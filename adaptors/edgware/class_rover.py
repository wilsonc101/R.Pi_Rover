class piRoverControls():
    def __init__(self):
        self.throttlePosition = None
        self.directionPosition = None
        self.brakeState = None
        self.vehicleLightState = None
        self.cameraPanPosition = None
        self.cameraTiltPosition = None
        self.cameraLightState = None


class piRoverVehicle():
    def __init__(self):
        self.vehcleWifi = None
        self.vehcleBatteryA = None
        self.vehcleBatteryB = None
        self.environmentTemperature = None
        self.environmentPressure = None
        self.gpsLatitude = None
        self.gpsLongitude = None
        self.gpsAltitude = None
        self.gpsSpeed = None
        self.accelLR = None
        self.accelRF = None

