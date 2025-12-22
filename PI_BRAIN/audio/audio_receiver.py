import speech_recognition as sr

class AudioReceiver:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_words = ["hey panda", "ok panda", "panda"]

        try:
            with self.microphone as source:
                print("[Audio] Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[Audio] Microphone ready")
        except Exception as e:
            print(f"[Audio] Warning: Could not calibrate microphone: {e}")

    def _is_wake_word(self, text: str) -> bool:
        text = text.lower()
        return any(wake in text for wake in self.wake_words)

    def listen_for_wake_word(self) -> bool:
        print("[Audio] Listening for wake word...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
            text = self.recognizer.recognize_google(audio)
            print(f"[Heard] {text}")
            return self._is_wake_word(text)
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return False
        except sr.RequestError as e:
            print(f"[Audio] STT error: {e}")
            return False

    def listen_for_command(self) -> str | None:
        print("[Audio] Listening for command...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = self.recognizer.recognize_google(audio)
            print(f"[Command] {text}")
            return text
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            print("[Audio] Could not understand command")
        except sr.RequestError as e:
            print(f"[Audio] STT error: {e}")
        return None
