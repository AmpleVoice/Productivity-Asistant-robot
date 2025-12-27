import time
import adafruit_dht
import threading

class DHT11Sensor:
    MIN_READ_INTERVAL = 2.0

    def __init__(self, board_pin):
        self.dht_device = adafruit_dht.DHT11(board_pin)
        self.latest_data = None
        self._last_read_time = 0
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        while not self._stop_event.is_set():
            now = time.time()
            if now - self._last_read_time >= self.MIN_READ_INTERVAL:
                try:
                    temp = self.dht_device.temperature
                    hum = self.dht_device.humidity
                    valid = temp is not None and hum is not None
                    if valid:
                        self._last_read_time = now
                except RuntimeError:
                    temp = hum = None
                    valid = False

                self.latest_data = {
                    "dht11": {
                        "temperature_c": round(temp, 1) if temp else None,
                        "humidity_pct": round(hum, 1) if hum else None
                    },
                    "timestamp": round(now, 2),
                    "valid": valid
                }

            time.sleep(0.5)

    def read(self):
        return self.latest_data