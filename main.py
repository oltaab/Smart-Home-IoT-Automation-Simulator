from smart_device_module import *
from central_automation_system_module import *

from dashboard import *
import tkinter as tk

light1 = SmartLight("Living Room Light")
thermostat1 = Thermostat("Living Room Thermostat")
camera1 = SecurityCamera("Living Room Security Camera")

automation_system = AutomationSystem()
automation_system.add_device(light1)
automation_system.add_device(thermostat1)
automation_system.add_device(camera1)

automation_system.start_data_gathering()

root = tk.Tk()
dashboard = Dashboard(root, automation_system)
dashboard.setup_log_area()
dashboard.start_log_monitoring()

root.mainloop()




