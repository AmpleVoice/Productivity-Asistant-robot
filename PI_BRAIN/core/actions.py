"""
actions.py - Pure hardware output commands.

This module is a THIN WRAPPER over hardware outputs.
NO LOGIC. NO STATE. NO THREADING. NO FALLBACKS.

Responsibilities:
- Send commands to motors (via serial)
- Send commands to speaker (TTS/beep)
- Send commands to LCD
- Send commands to LEDs/buzzer (shift register)

NOT responsible for:
- GPIO initialization (handled by startup.py)
- Speed limits (handled by MovementController)
- Threading (handled by AudioManager)
- Error recovery (handled by callers)
"""

# Hardware interfaces (injected by startup.py)
_serial = None
_speaker = None
_lcd = None
_shift_register = None


def bind_hardware(serial=None, speaker=None, lcd=None, shift_register=None):
    """
    Inject hardware interfaces.
    Called once by startup.py after hardware initialization.
    """
    global _serial, _speaker, _lcd, _shift_register
    _serial = serial
    _speaker = speaker
    _lcd = lcd
    _shift_register = shift_register


# =============================================================================
# MOTORS (Serial Commands)
# =============================================================================

def motors_set(left_speed: int, right_speed: int):
    """
    Set motor speeds via serial.
    
    Args:
        left_speed: -255 to 255 (negative = reverse)
        right_speed: -255 to 255 (negative = reverse)
    
    Sends: M:left_speed:right_speed\n
    """
    if _serial is None:
        return
    
    try:
        command = f"M:{left_speed}:{right_speed}\n"
        _serial.write(command.encode())
    except Exception:
        pass  # Silent fail - caller handles errors


def motors_stop():
    """
    Stop all motors immediately.
    
    Sends: S\n
    """
    if _serial is None:
        return
    
    try:
        _serial.write(b"S\n")
    except Exception:
        pass


def camera_set_angle(angle: int):
    """
    Set camera servo angle.
    
    Args:
        angle: 0-180 degrees
    
    Sends: C:angle\n
    """
    if _serial is None:
        return
    
    try:
        command = f"C:{angle}\n"
        _serial.write(command.encode())
    except Exception:
        pass


# =============================================================================
# SPEAKER (TTS / Beep)
# =============================================================================

def speaker_say(text: str):
    """
    Speak text via TTS.
    
    Args:
        text: Text to speak
    
    Note: This is BLOCKING. Caller should handle threading if needed.
    """
    if _speaker is None:
        return
    
    try:
        _speaker.say(text)
    except Exception:
        pass


def speaker_beep():
    """
    Play short beep sound.
    """
    if _speaker is None:
        return
    
    try:
        _speaker.beep()
    except Exception:
        pass


# =============================================================================
# LCD (16x2 Display)
# =============================================================================

def lcd_write(line: int, text: str):
    """
    Write text to LCD line.
    
    Args:
        line: 0 or 1 (top or bottom)
        text: Text to display (no truncation - caller handles)
    """
    if _lcd is None:
        return
    
    try:
        _lcd.write(line, text)
    except Exception:
        pass


def lcd_clear():
    """
    Clear LCD display.
    """
    if _lcd is None:
        return
    
    try:
        _lcd.clear()
    except Exception:
        pass


# =============================================================================
# LEDs + BUZZER (Shift Register)
# =============================================================================

def leds_set(mask: int):
    """
    Set LED states via shift register.
    
    Args:
        mask: 20-bit integer where each bit controls one LED
              Bit mapping defined in settings.py
    
    Example:
        leds_set(0b00000000000000000011)  # Turn on LED 0 and 1
    """
    if _shift_register is None:
        return
    
    try:
        _shift_register.set_leds(mask)
    except Exception:
        pass


def buzzer_on():
    """
    Turn buzzer on.
    """
    if _shift_register is None:
        return
    
    try:
        _shift_register.buzzer_on()
    except Exception:
        pass


def buzzer_off():
    """
    Turn buzzer off.
    """
    if _shift_register is None:
        return
    
    try:
        _shift_register.buzzer_off()
    except Exception:
        pass


# =============================================================================
# HARDWARE TEST HELPERS (for startup.py validation only)
# =============================================================================

def hardware_test_beep():
    """
    Minimal beep for hardware validation.
    Does NOT use normal speaker interface.
    """
    try:
        import time
        if _shift_register:
            _shift_register.buzzer_on()
            time.sleep(0.1)
            _shift_register.buzzer_off()
    except Exception:
        pass


def hardware_test_lcd():
    """
    Minimal LCD test for hardware validation.
    """
    try:
        if _lcd:
            _lcd.write(0, "TEST")
            import time
            time.sleep(0.5)
            _lcd.clear()
    except Exception:
        pass