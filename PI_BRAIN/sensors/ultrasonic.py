# ultrasonic.py
import RPi.GPIO as GPIO
import time
import threading

class UltrasonicArray:
    SPEED_OF_SOUND = 34300  # cm/s

    def __init__(self, sensors: dict, settle_time: float = 0.05):
        self.sensors = sensors
        self.settle_time = settle_time
        # Initialize with a safe default so non-Pi dev runs have values
        self.latest_data = {
            "ultrasonic": {name: 100 for name in self.sensors.keys()},
            "timestamp": round(time.time(), 2),
            "valid": True
        }
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

        GPIO.setmode(GPIO.BCM)
        for s in self.sensors.values():
            GPIO.setup(s["trig"], GPIO.OUT)
            GPIO.setup(s["echo"], GPIO.IN)
            GPIO.output(s["trig"], False)

        time.sleep(2)
        self._thread.start()

    def _measure_distance(self, trig, echo):
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        start = time.time()
        timeout = start + 0.03

        while GPIO.input(echo) == 0:
            if time.time() > timeout:
                return None
            start = time.time()

        while GPIO.input(echo) == 1:
            if time.time() > timeout:
                return None
            end = time.time()

        duration = end - start
        return round((duration * self.SPEED_OF_SOUND) / 2, 2)

    def _loop(self):
        while not self._stop_event.is_set():
            data = {}
            valid = True

            for name, pins in self.sensors.items():
                dist = self._measure_distance(pins["trig"], pins["echo"])
                time.sleep(self.settle_time)
                if dist is None:
                    # Keep previous reading if available, otherwise use a safe default
                    prev = self.latest_data.get("ultrasonic", {}).get(name, 100)
                    data[name] = prev
                    valid = False
                else:
                    data[name] = dist

            self.latest_data = {
                "ultrasonic": data,
                "timestamp": round(time.time(), 2),
                "valid": valid
            }

    def read(self):
        return self.latest_data

    def cleanup(self):
        self._stop_event.set()
        GPIO.cleanup()
