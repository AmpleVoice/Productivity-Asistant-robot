# PI_BRAIN/audio_test.py

import sys
import platform

# If not on a Raspberry Pi, mock the GPIO library
if platform.system() != "Linux":
    try:
        import mocked
        sys.modules['RPi'] = mocked
        sys.modules['RPi.GPIO'] = mocked.GPIO
        print("[Mock] RPi.GPIO module mocked for non-Linux system.")
    except ImportError:
        print("[Mock] Warning: mocked.py not found. GPIO calls may fail.")

import time
from core.decision_engine import DecisionEngine
from audio.audio_manager import AudioManager

class MockRobotSensors:
    """
    A mock sensor class for testing the audio system on Windows
    without needing the actual robot hardware.
    """
    def read(self):
        # Return a dictionary with a dummy temperature reading
        return {
            "temperature": 22.5
        }

def main():
    """
    Main function to run the audio test.
    """
    print("--- Robot Audio System Test ---")
    print("This program will test the audio listening and speech processing loop.")
    print("The robot's hardware (sensors, motors) is mocked.")
    print("Say 'Hey Panda' to wake the robot up, then give a command.")
    print("Supported commands: 'hello', 'how are you', 'temperature', 'time', 'date', 'follow', 'stop'.")
    print("Press Ctrl+C to exit.")

    # 1. Create mock sensors
    mock_sensors = MockRobotSensors()

    # 2. Initialize the decision engine with the mock sensors
    decision_engine = DecisionEngine(mock_sensors)

    # 3. Initialize the audio manager with the decision engine
    audio_manager = AudioManager(decision_engine)

    # 4. Start the audio manager in a background thread
    audio_manager.start_async()

    # 5. Keep the main thread alive to let the background thread run
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- Exiting audio test ---")
        audio_manager.stop()

if __name__ == "__main__":
    main()
