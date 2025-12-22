# sensors.py
from mq9 import MQ9Sensor
from ultrasonic import UltrasonicArray
from gps import GPSModule
from dht11 import DHT11Sensor
from config.settings import *
import board

class RobotSensors:
    def __init__(self):
        self.mq9 = MQ9Sensor(MQ9_SENSOR_PIN)
        self.ultrasonic = UltrasonicArray({
            "left": {"trig": LEFT_ULTRASONIC_SENSOR_TRIG_PIN, "echo": LEFT_ULTRASONIC_SENSOR_ECHO_PIN},
            "right": {"trig": RIGHT_ULTRASONIC_SENSOR_TRIG_PIN, "echo": RIGHT_ULTRASONIC_SENSOR_ECHO_PIN}
        })
        self.gps = GPSModule(GPS_MODULE_PORT)
        self.dht11 = DHT11Sensor(board.D4)

    def read(self):
        return {
            "ultrasonic": self.ultrasonic.read(),
            "gps": self.gps.read(),
            "environment": self.dht11.read(),
            "gas": self.mq9.read()
        }

    def cleanup(self):
        self.mq9.cleanup()
        self.ultrasonic.cleanup()
        self.gps.close()
