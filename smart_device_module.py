from enum import Enum


class Status(Enum):
    OFF = "Off"
    ON = "On"


class Motion(Enum):
    YES = "Yes"
    NO = "No"


class Device:
    def __init__(self, device_id):
        self._device_id = device_id
        self.status = Status.OFF

    def get_device_id(self):
        return self._device_id

    def turn_on(self):
        if self.status == Status.OFF:
            self.status = Status.ON
        else:
            print("Device Is Turned ON Already")

    def turn_off(self):
        if self.status == Status.ON:
            self.status = Status.OFF
        else:
            print("Device Is Turned OFF Already")

    def printable(self):
        return f"{self.get_device_id()} : {self.__class__.__name__} Status: {self.status.value}\n"


class SmartLight(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 0

    def set_brightness(self, num):
        if 0 <= num <= 100:
            self.brightness = num
        else:
            print("RANGE OF SMART LIGHT IS 0 <= N <= 100")


class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 0

    def set_temperature(self, num):
        if 10 <= num <= 30:
            self.temperature = num
        else:
            print("RANGE OF THERMOSTAT IS 10 <= N <= 30")


class SecurityCamera(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.motion = Motion.NO

    def set_security_status(self, status):
        self.motion = status
