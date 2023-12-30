# Part 2: Central Automation System (25 %)
import random
import time
from smart_device_module import *
import threading
import random
import time
from smart_device_module import *


class AutomationSystem:
    def __init__(self):
        self.smart_light = None
        self.thermostat = None
        self.security_camera = None
        self.status = Status.OFF

    def add_device(self, device):
        if isinstance(device, SmartLight):
            self.smart_light = device
        elif isinstance(device, Thermostat):
            self.thermostat = device
        elif isinstance(device, SecurityCamera):
            self.security_camera = device
        else:
            print("NOT A LEGITIMATE DEVICE")

    def turn_on(self):
        if self.status == Status.OFF:
            self.status = Status.ON
            self.turn_on_all()
        else:
            print("Device Is Turned ON Already")

    def turn_off(self):
        if self.status == Status.ON:
            self.status = Status.OFF
            self.turn_off_all()
        else:
            print("Device Is Turned OFF Already")

    def automatic_events(self):
        if self.security_camera.security_status == Motion.YES:
            self.smart_light.turn_on()

    def simulate_device_changes(self):
        while True:
            self.smart_light.set_brightness(random.randint(0, 100))
            self.thermostat.set_temperature(random.uniform(10.0, 30.0))
            self.security_camera.set_security_status(random.choice([Motion.YES, Motion.NO]))
            time.sleep(5)

    def current_state(self):
        the_string = ""
        the_string += self.smart_light.printable()
        the_string += self.security_camera.printable()
        the_string += self.thermostat.printable()
        return the_string

    def data_gathering_to_file(self):
        with open("sensor_data.txt", "a") as f:
            f.write(str(self.smart_light.__dict__))
            f.write(str(self.security_camera.__dict__))
            f.write(str(self.thermostat.__dict__))

    def turn_off_all(self):
        self.smart_light.turn_off()
        self.security_camera.turn_off()
        self.thermostat.turn_off()

    def turn_on_all(self):
        self.smart_light.turn_on()
        self.security_camera.turn_on()
        self.thermostat.turn_on()

    def data_gathering_to_file(self, filename="sensor_data.txt"):
        # Formatting the data as a CSV string
        data_string = f"{time.strftime('%Y-%m-%d %H:%M:%S')},"
        data_string += f"{self.smart_light.get_device_id()}, {self.smart_light.status.value}, {self.smart_light.brightness},"
        data_string += f"{self.thermostat.get_device_id()}, {self.thermostat.status.value}, {self.thermostat.temperature},"
        data_string += f"{self.security_camera.get_device_id()}, {self.security_camera.status.value}, {self.security_camera.motion.value}\n"

        with open(filename, "a") as file:
            file.write(data_string)

    def start_data_gathering(self):
        def gather_data():
            while True:
                self.data_gathering_to_file()
                time.sleep(5)

        # Start the gathering thread
        data_thread = threading.Thread(target=gather_data)
        data_thread.daemon = True
        data_thread.start()

