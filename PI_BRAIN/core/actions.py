import RPi.GPIO as GPIO
import time

# Configure your GPIO pins here
# For example:
# MOTOR_LEFT_FORWARD = 17
# MOTOR_LEFT_BACKWARD = 27
# ... etc.

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # Setup your pins as output
    # GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
    # ... etc.


def stop():
    print("Action: Stop")
    # Add your GPIO logic here
    pass

def ring_alarm():
    print("Action: Ring Alarm")
    # Add your GPIO logic for a buzzer here
    pass

def play_sound(name):
    """Play a small named sound (beep) for testing."""
    print(f"Action: Play sound '{name}'")

def lcd_display(text, line=0):
    """Stub for LCD display - test-only."""
    print(f"LCD[{line}]: {text}")

def lcd_clear():
    print("LCD: clear")

def stop_motors():
    print("Action: Stop motors")
    stop()

def set_motor_speeds(left_speed, right_speed):
    """Set motor speeds (left, right). This is a simple stub for testing.
    Real implementation should convert to PWM and respect motor mapping.
    """
    print(f"Action: Set motor speeds L={left_speed} R={right_speed}")

def set_camera_angle(angle):
    print(f"Action: Set camera angle to {angle}")

# Simple cross-platform TTS using pyttsx3 (non-blocking)
_tts_engine = None

def _init_tts():
    global _tts_engine
    try:
        import pyttsx3
    except Exception:
        _tts_engine = None
        return
    _tts_engine = pyttsx3.init()

def _run_tts(text):
    global _tts_engine
    if _tts_engine is None:
        _init_tts()
        if _tts_engine is None:
            # Fallback for Windows: use PowerShell SAPI to speak if available
            try:
                import os
                if os.name == 'nt':
                    import subprocess
                    cmd = ['powershell', '-Command', "Add-Type -AssemblyName System.Speech;" \
                           f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}')"]
                    subprocess.Popen(cmd)
                    return
            except Exception:
                pass
            print(f"TTS unavailable: {text}")
            return
    try:
        _tts_engine.say(text)
        _tts_engine.runAndWait()
    except Exception as e:
        print(f"TTS error: {e}")

def talk(text):
    print(f"Action: Speak '{text}'")
    # Run TTS in a background thread so it doesn't block the main loop
    import threading
    t = threading.Thread(target=_run_tts, args=(text,), daemon=True)
    t.start()

# Call this once at the start of your program
# setup_gpio()