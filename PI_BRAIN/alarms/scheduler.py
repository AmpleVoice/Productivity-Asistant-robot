import threading, time
from datetime import datetime
from config.settings import *

class Scheduler(threading.Thread):
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.running = True

    def run(self):
        while self.running:
            now = datetime.now().strftime("%H:%M")
            if now == "07:00":
                self.callback("ALARM")
            time.sleep(SCHEDULER_INTERVAL)
