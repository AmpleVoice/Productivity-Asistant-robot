import threading
from audio.audio_receiver import AudioReceiver

class AudioManager:
    def __init__(self, decision_engine):
        self.audio = AudioReceiver()
        self.engine = decision_engine
        self.running = False
        self.thread = None

    def run(self):
        self.running = True
        print("[AudioManager] Started")
        while self.running:
            try:
                if not self.audio.listen_for_wake_word():
                    continue
                command = self.audio.listen_for_command()
                if command:
                    self.engine.handle_voice(command)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"[AudioManager] Error: {e}")

    def start_async(self):
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        print("[AudioManager] Running in background thread")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
