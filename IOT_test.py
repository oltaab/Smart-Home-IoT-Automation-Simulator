import unittest
from central_automation_system_module import AutomationSystem, Status, Motion
from smart_device_module import SmartLight, Thermostat, SecurityCamera

class TestAutomationSystem(unittest.TestCase):
    def setUp(self):
        # Set up the system and devices for testing
        self.light = SmartLight("Test Light")
        self.thermostat = Thermostat("Test Thermostat")
        self.camera = SecurityCamera("Test Camera")

        self.system = AutomationSystem()
        self.system.add_device(self.light)
        self.system.add_device(self.thermostat)
        self.system.add_device(self.camera)

    # Test Cases for Smart Light
    def test_light_on_off(self):
        self.light.turn_on()
        self.assertEqual(self.light.status, Status.ON)
        self.light.turn_off()
        self.assertEqual(self.light.status, Status.OFF)

    def test_adjust_brightness(self):
        self.light.set_brightness(50)
        self.assertEqual(self.light.brightness, 50)

    # Test Cases for Thermostat
    def test_thermostat_on_off(self):
        self.thermostat.turn_on()
        self.assertEqual(self.thermostat.status, Status.ON)
        self.thermostat.turn_off()
        self.assertEqual(self.thermostat.status, Status.OFF)

    def test_adjust_temperature(self):
        self.thermostat.set_temperature(20)
        self.assertEqual(self.thermostat.temperature, 20)

    # Test Cases for Security Camera
    def test_camera_on_off(self):
        self.camera.turn_on()
        self.assertEqual(self.camera.status, Status.ON)
        self.camera.turn_off()
        self.assertEqual(self.camera.status, Status.OFF)

    def test_motion_detection(self):
        self.camera.set_security_status(Motion.YES)
        self.assertEqual(self.camera.motion, Motion.YES)

    # Test Cases for Automation System
    def test_system_on_off(self):
        self.system.turn_on()
        self.assertEqual(self.system.status, Status.ON)
        self.system.turn_off()
        self.assertEqual(self.system.status, Status.OFF)

    def test_automation_response(self):
        self.system.turn_on()
        self.camera.set_security_status(Motion.YES)
        self.system.automatic_events()
        self.assertEqual(self.light.status, Status.ON)


if __name__ == '__main__':
    unittest.main()
