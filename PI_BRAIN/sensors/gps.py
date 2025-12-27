import serial
import threading
import time

class GPSModule:
    def __init__(self, port, baudrate=9600):
        self.serial = serial.Serial(port, baudrate, timeout=1)
        self.latest_data = None

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _parse_nmea(self, line):
        if not line.startswith("$GPGGA"):
            return None

        parts = line.split(",")
        if len(parts) < 6 or parts[2] == "" or parts[4] == "":
            return None

        lat = parts[2]
        lon = parts[4]

        return {
            "latitude_raw": lat,
            "longitude_raw": lon
        }

    def _loop(self):
        while not self._stop_event.is_set():
            try:
                line = self.serial.readline().decode("ascii", errors="ignore").strip()
                parsed = self._parse_nmea(line)
                if parsed:
                    self.latest_data = {
                        "gps": parsed,
                        "timestamp": round(time.time(), 2),
                        "valid": True
                    }
            except Exception:
                pass

    def read(self):
        return self.latest_data

    def close(self):
        self._stop_event.set()
        if self.serial.is_open:
            self.serial.close()