import json
import time
import threading
from datetime import datetime
import pygame

CONFIG_PATH = "config/scheduler.json"
SOUND_PATH = "sounds/alarm.mp3"

class AlarmRunner(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = True
        self.last_triggered = {}
        self.alarm_playing = False
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(SOUND_PATH)
        except pygame.error:
            print(f"⚠️ Audio file '{SOUND_PATH}' not found. Sound will not play.")

    def run(self):
        print("⏰ Alarm monitoring thread started")
        while self.running:
            self.check_alarms()
            time.sleep(1)

    def check_alarms(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        now = datetime.now().strftime("%H:%M")

        for alarm_id, alarm in data["alarms"].items():
            if not alarm["enabled"]:
                continue

            if alarm["time"] == now:
                # Prevent multiple triggers per minute
                if self.last_triggered.get(alarm_id) != now:
                    print(f"🚨 ALARM TRIGGERED: {alarm_id} at {now}")
                    self.play_alarm()
                    self.last_triggered[alarm_id] = now

    def play_alarm(self):
        """Play the alarm sound in infinite loop"""
        try:
            if not self.alarm_playing:
                pygame.mixer.music.play(loops=-1)  # Infinite loop
                self.alarm_playing = True
                print("🔊 Alarm sound playing (infinite loop)...")
                print("   Type 'stop alarm' to stop the sound")
        except Exception as e:
            print(f"❌ Error playing sound: {e}")

    def stop_alarm(self):
        """Stop the alarm sound"""
        if self.alarm_playing:
            pygame.mixer.music.stop()
            self.alarm_playing = False
            print("🔇 Alarm stopped")
        else:
            print("ℹ️ No alarm is currently playing")

    def stop(self):
        self.running = False
        pygame.mixer.music.stop()
        print("⏹️ Alarm monitoring thread stopped")
