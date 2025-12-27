"""
sensor.py - Unified sensor interface with STABLE schema.

This module provides a single, consistent interface to all robot sensors.
The schema returned by read() is FROZEN and trusted by all consumers.
"""

from sensors.mq9 import MQ9Sensor
from sensors.ultrasonic import UltrasonicArray
from sensors.gps import GPSModule
from sensors.dht11 import DHT11Sensor
from config.settings import *
import board

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except Exception:
    GPIO_AVAILABLE = False
    # Try dev_mocks if available
    import sys
    dm = sys.modules.get('dev_mocks')
    if dm and getattr(dm, 'gpio', None):
        GPIO = dm.gpio
        GPIO_AVAILABLE = True


class RobotSensors:
    """
    Central sensor interface.
    
    Returns STABLE schema via read() method.
    All consumers (startup, decision engine) trust this schema.
    """
    
    def __init__(self):
        # Initialize all sensor modules
        self.mq9 = MQ9Sensor(MQ9_SENSOR_PIN)
        self.ultrasonic = UltrasonicArray({
            "left": {"trig": LEFT_ULTRASONIC_SENSOR_TRIG_PIN, "echo": LEFT_ULTRASONIC_SENSOR_ECHO_PIN},
            "right": {"trig": RIGHT_ULTRASONIC_SENSOR_TRIG_PIN, "echo": RIGHT_ULTRASONIC_SENSOR_ECHO_PIN}
        })
        self.gps = GPSModule(GPS_MODULE_PORT)
        self.dht11 = DHT11Sensor(board.D4)
        
        # Initialize orientation sensor (flip detector)
        self._orientation_pin = getattr(settings, 'FLIP_SENSOR_PIN', None)
        self._orientation_available = False
        
        if self._orientation_pin is not None and GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                try:
                    GPIO.setup(self._orientation_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                except TypeError:
                    # Some GPIO implementations don't accept keyword args
                    GPIO.setup(self._orientation_pin, GPIO.IN)
                self._orientation_available = True
            except Exception:
                self._orientation_available = False

    def read(self):
        """
        Read all sensors and return STABLE schema.
        
        Returns:
            dict: Sensor data in frozen format:
            {
                "ultrasonic": {
                    "left": float or None,   # cm (2-400)
                    "right": float or None   # cm (2-400)
                },
                "dht11": {
                    "temperature_c": float or None,  # Celsius
                    "humidity": float or None        # Percent (0-100)
                },
                "mq9": {
                    "co_ppm": float or None,  # Parts per million
                    "dangerous": bool         # True if CO exceeds threshold
                },
                "gps": {
                    "latitude": float or None,
                    "longitude": float or None,
                    "altitude": float or None,
                    "speed": float or None,
                    "fix": bool  # True if GPS has valid fix
                },
                "orientation": {
                    "flipped": bool,      # True if robot is upside down
                    "available": bool     # True if sensor is working
                }
            }
        """
        # Read ultrasonic sensors
        ultrasonic_raw = self.ultrasonic.read()
        ultrasonic_data = ultrasonic_raw.get("ultrasonic", {})
        
        # Read DHT11 (temperature/humidity)
        dht_raw = self.dht11.read()
        dht_data = dht_raw.get("dht11", {})
        
        # Read MQ9 (gas sensor)
        mq9_raw = self.mq9.read()
        mq9_data = mq9_raw.get("mq9", {})
        
        # Read GPS
        gps_raw = self.gps.read()
        gps_data = gps_raw.get("gps", {})
        
        # Read orientation (flip sensor)
        orientation = self._read_orientation()
        
        # Return STABLE schema
        return {
            "ultrasonic": {
                "left": ultrasonic_data.get("left"),
                "right": ultrasonic_data.get("right")
            },
            "dht11": {
                "temperature_c": dht_data.get("temperature"),
                "humidity": dht_data.get("humidity")
            },
            "mq9": {
                "co_ppm": mq9_data.get("co_ppm"),
                "dangerous": mq9_data.get("dangerous_CO", False)
            },
            "gps": {
                "latitude": gps_data.get("latitude"),
                "longitude": gps_data.get("longitude"),
                "altitude": gps_data.get("altitude"),
                "speed": gps_data.get("speed"),
                "fix": gps_data.get("latitude") is not None
            },
            "orientation": orientation
        }
    
    def _read_orientation(self):
        """
        Read orientation sensor (flip detector).
        
        The flip sensor is a simple conductor that connects when upside down.
        When flipped: GPIO reads HIGH (1)
        When normal: GPIO reads LOW (0)
        
        Returns:
            dict: {"flipped": bool, "available": bool}
        """
        if not self._orientation_available or self._orientation_pin is None:
            return {
                "flipped": False,  # Assume correct orientation if sensor unavailable
                "available": False
            }
        
        try:
            is_flipped = bool(GPIO.input(self._orientation_pin))
            return {
                "flipped": is_flipped,
                "available": True
            }
        except Exception:
            return {
                "flipped": False,
                "available": False
            }

    def cleanup(self):
        """Clean up all sensor resources."""
        self.mq9.cleanup()
        self.ultrasonic.cleanup()
        self.gps.close()
        
        # GPIO cleanup handled by main shutdown (single owner)