# PI_BRAIN/audio/audio_test.py

from core.decision_engine import DecisionEngine

# ---- MOCK SENSORS (Laptop-safe) ----
class MockSensors:
    emergency = False
    gas_danger = False
    temperature = 22

# ---- MOCK ACTIONS OUTPUT ----
import core.actions as actions

def mock_talk(text):
    print(f"[PANDA] {text}")

actions.talk = mock_talk

# ---- RUN AUDIO SYSTEM ----
from audio.audio_manager import AudioManager

if __name__ == "__main__":
    sensors = MockSensors()
    engine = DecisionEngine(sensors)

    audio = AudioManager(engine)
    audio.run()
