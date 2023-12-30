import tkinter as tk
from tkinter import ttk
import threading
import time

from central_automation_system_module import *


class Dashboard:
    def __init__(self, root, system):
        self.root = root
        self.system = system

        self.automation_status = tk.StringVar()
        self.update_automation_status()

        self.current_state_of_devices = tk.StringVar()
        self.current_state_of_devices.set(self.system.current_state())

        root.geometry("800x800")
        root.title("Smart Home IoT Simulator")

        button = tk.Button(root, text="Automation ON/OFF", font=('Arial', 18), command=self.system_change_status)
        button.pack()

        label1 = tk.Label(self.root, textvariable=self.automation_status, font=('Arial', 18))
        label1.pack()

        label2 = tk.Label(self.root, textvariable=self.current_state_of_devices, font=('Arial', 18))
        label2.pack()

        # SmartLight
        # "ID + brightness"
        self.device_id_var_light = tk.StringVar()
        self.device_id_var_light.set(self.system.smart_light.get_device_id() + " Brightness")

        label3 = tk.Label(self.root, textvariable=self.device_id_var_light, font=('Arial', 18))
        label3.pack()

        # Scale
        w_light = tk.Scale(self.root, from_=0, to=100, orient='horizontal', command=self.update_brightness_label)
        w_light.pack()

        # Toggle button
        button_light = tk.Button(self.root, text="Toggle ON/OFF", font=('Arial', 18),
                                 command=self.button_light_change_status)
        button_light.pack()

        # "Living room light - (the scale number)%"
        device_id_var_light2 = tk.StringVar()
        device_id_var_light2.set(f"{self.system.smart_light.get_device_id()} - {self.system.smart_light.brightness} %")

        label4 = tk.Label(self.root, textvariable=device_id_var_light2, font=('Arial', 18))
        label4.pack(pady=30)

        self.device_id_var_light2 = device_id_var_light2
        self.w_light = w_light

        # Thermostat
        # "ID + temperature"
        self.device_id_var_thermo = tk.StringVar()
        self.device_id_var_thermo.set(self.system.thermostat.get_device_id() + " Temperature")

        label5 = tk.Label(self.root, textvariable=self.device_id_var_thermo, font=('Arial', 18))
        label5.pack()

        w_thermo = tk.Scale(self.root, from_=10, to=30, orient='horizontal', command=self.update_temperature_label)
        w_thermo.pack()

        button_thermo = tk.Button(self.root, text="Toggle ON/OFF", font=('Arial', 18),
                                  command=self.button_thermo_change_status)
        button_thermo.pack()

        self.device_id_var_thermo2 = tk.StringVar()
        self.device_id_var_thermo2.set(
            f"{self.system.thermostat.get_device_id()} - {self.system.thermostat.temperature}°C")

        label6 = tk.Label(self.root, textvariable=self.device_id_var_thermo2, font=('Arial', 18))
        label6.pack(pady=30)
        self.w_thermo = w_thermo

        # Front Door Camera
        self.device_id_var_camera = tk.StringVar()
        self.device_id_var_camera.set(self.system.security_camera.get_device_id() + " Detection")

        label7 = tk.Label(self.root, textvariable=self.device_id_var_camera, font=('Arial', 18))
        label7.pack()

        button_camera_random = tk.Button(self.root, text="Random Detect Motion", font=('Arial', 18),
                                         command=self.start_simulation)
        button_camera_random.pack()

        button_camera = tk.Button(self.root, text="Toggle ON/OFF", font=('Arial', 18),
                                  command=self.button_security_camera_change_status)
        button_camera.pack()

        self.device_id_var_camera2 = tk.StringVar()
        self.device_id_var_camera2.set(f"{self.system.security_camera.get_device_id()} - Motion: "
                                       f"{self.system.security_camera.motion.value}")

        label8 = tk.Label(self.root, textvariable=self.device_id_var_camera2, font=('Arial', 18))
        label8.pack()

        label9 = tk.Label(self.root, text="Automation Rule: TURN ON LIGHTS WHEN MOTION IS DETECTED", font=('Arial', 18))
        label9.pack()

    def start_simulation(self):
        def run_simulation():
            while True:
                self.system.turn_on_all()
                self.current_state_of_devices.set(self.system.current_state())

                self.system.smart_light.set_brightness(random.randint(0, 100))
                self.system.thermostat.set_temperature(random.uniform(10.0, 30.0))
                self.system.security_camera.set_security_status(random.choice([Motion.YES, Motion.NO]))

                self.device_id_var_light2.set(
                    f"{self.system.smart_light.get_device_id()} - {self.system.smart_light.brightness} %")
                self.device_id_var_thermo2.set(
                    f"{self.system.thermostat.get_device_id()} - {self.system.thermostat.temperature}°C")
                self.device_id_var_camera2.set(
                    f"{self.system.security_camera.get_device_id()} - Motion: {self.system.security_camera.motion.value}")

                self.w_light.set(self.system.smart_light.brightness)
                self.w_thermo.set(int(self.system.thermostat.temperature))

                self.root.update_idletasks()
                time.sleep(2)

        simulation_thread = threading.Thread(target=run_simulation)
        simulation_thread.daemon = True
        simulation_thread.start()

    def random_detect_motion(self):
        if self.system.security_camera.status == Status.ON:
            self.system.security_camera.set_security_status(Motion.YES)
            self.device_id_var_camera2.set(f"{self.system.security_camera.get_device_id()} - Motion: "
                                           f"{self.system.security_camera.motion.value}")
            self.system.smart_light.turn_on()  # Turn on the lights when motion is detected
            self.root.after(5000, self.turn_off_random_motion)
            self.current_state_of_devices.set(self.system.current_state())

    def turn_off_random_motion(self):
        self.system.security_camera.set_security_status(Motion.NO)
        self.device_id_var_camera2.set(f"{self.system.security_camera.get_device_id()} - Motion: "
                                       f"{self.system.security_camera.motion.value}")

        self.system.smart_light.turn_off()
        self.current_state_of_devices.set(self.system.current_state())

    def update_temperature_label(self, value):
        if self.system.thermostat.status == Status.ON:  # Check if the thermostat is ON
            temperature = int(value)
            self.system.thermostat.set_temperature(temperature)
            self.device_id_var_thermo2.set(f"{self.system.thermostat.get_device_id()} - {temperature}°C")
            self.w_thermo.set(temperature)

    def update_brightness_label(self, value):
        if self.system.smart_light.status == Status.ON:  # Check if the smart light is ON
            brightness = int(value)
            self.system.smart_light.set_brightness(brightness)
            self.device_id_var_light2.set(f"{self.system.smart_light.get_device_id()} - {brightness}%")
            self.w_light.set(brightness)

    def button_thermo_change_status(self):
        if self.system.thermostat.status == Status.OFF:
            self.system.thermostat.turn_on()
            self.w_thermo.set(self.system.thermostat.temperature)  # Update the Scale to the current temperature
        else:
            self.system.thermostat.turn_off()
            self.w_thermo.set(0)  # Set the Scale to 0 when the device is turned off
        self.current_state_of_devices.set(self.system.current_state())
        self.device_id_var_thermo2.set(
            f"{self.system.thermostat.get_device_id()} - {self.system.thermostat.temperature}°C")

    def update_automation_status(self):
        self.automation_status.set("Automation Status: " + self.system.status.value)

    def system_change_status(self):
        if self.system.status == Status.OFF:
            self.system.turn_on()
        else:
            self.system.turn_off()
        self.update_automation_status()

    def button_light_change_status(self):
        if self.system.smart_light.status == Status.OFF:
            self.system.smart_light.turn_on()
            self.w_light.set(self.system.smart_light.brightness)
        else:
            self.system.smart_light.turn_off()
            self.w_light.set(0)
        self.current_state_of_devices.set(self.system.current_state())

    def button_security_camera_change_status(self):
        if self.system.security_camera.status == Status.OFF:
            self.system.security_camera.turn_on()
        else:
            self.system.security_camera.turn_off()
        self.current_state_of_devices.set(self.system.current_state())

    def setup_log_area(self):
        # Create a frame for the log area
        log_frame = ttk.Frame(self.root)
        log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create the Text widget and pack it into the frame
        self.log_text = tk.Text(log_frame, height=6, width=50)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar and set it up next to the Text widget
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Connect the scrollbar to the text widget
        self.log_text['yscrollcommand'] = scrollbar.set

    def start_log_monitoring(self):
        def monitor_log_file():
            with open("sensor_data.txt", "r") as file:
                # Seek to the end of the file
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if line:
                        # This ensures the GUI updates are done in the main thread
                        self.log_text.insert(tk.END, line)
                        self.log_text.see(tk.END)
                        self.log_text.update_idletasks()
                    else:
                        time.sleep(1)  # Wait a bit before checking for new content

        # Start the thread that monitors the log file
        log_thread = threading.Thread(target=monitor_log_file, daemon=True)
        log_thread.start()


