# mq9.py
import RPi.GPIO as GPIO
import time
import threading

class MQ9Sensor:
    def __init__(self, pin):
        self.pin = pin
        self.latest_data = None
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        self._thread.start()

    def _loop(self):
        while not self._stop_event.is_set():
            dangerous = GPIO.input(self.pin) == GPIO.HIGH
            self.latest_data = {
                "mq9": {"dangerous_CO": dangerous},
                "timestamp": round(time.time(), 2),
                "valid": True
            }
            time.sleep(1)

    def read(self):
        return self.latest_data

    def cleanup(self):
        self._stop_event.set()
        GPIO.cleanup()
