# lcd.py
import threading
import time

class LCD16x2:
    def __init__(self):
        self.current_state = "IDLE"
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        while not self._stop_event.is_set():
            # later: draw Panda face here
            time.sleep(0.5)

    def update_state(self, state):
        self.current_state = state

    def stop(self):
        self._stop_event.set()
