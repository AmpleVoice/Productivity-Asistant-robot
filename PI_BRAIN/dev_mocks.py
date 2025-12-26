"""Development hardware mocks to allow running sensor code on non-Raspberry platforms (Windows).
Call install_mocks() early (before importing hardware-dependent modules).
"""
from types import ModuleType
import sys
import time

# Simple GPIO mock
class _GPIO:
    BCM = 'BCM'
    OUT = 'OUT'
    IN = 'IN'
    HIGH = 1
    LOW = 0
    PUD_DOWN = 'PUD_DOWN'
    PUD_UP = 'PUD_UP'

    def __init__(self):
        self._pin_states = {}
        self._last_trig_times = {}
        self._flip = False

    def setmode(self, mode):
        return None

    def setup(self, pin, mode, pull_up_down=None):
        # Accept None pins gracefully in dev mode
        self._pin_states[pin] = 0

    def output(self, pin, value):
        self._pin_states[pin] = 1 if value else 0
        # record last trig time for distance sim
        try:
            if value:
                self._last_trig_times[pin] = time.time()
        except Exception:
            pass

    def input(self, pin):
        # Flip sensor read
        if pin is None:
            return 0

        # If user set flip
        if pin == 'FLIP_SENSOR_PIN':
            return 1 if self._flip else 0

        # Ultrasonic echo simulation based on recent trig events
        now = time.time()
        # Find the most recent trig time
        if self._last_trig_times:
            last_trig = min(self._last_trig_times.values())
            elapsed = now - last_trig
            # Simulate: short pulse -> 0 then 1 then 0 to mimic echo
            if elapsed < 0.0005:
                return 0
            if elapsed < 0.003:
                return 1
            return 0

        # Default: return 0 (no signal)
        return 0

    def cleanup(self):
        self._pin_states.clear()
        self._last_trig_times.clear()

    # Helpers
    def set_flip(self, flipped: bool):
        self._flip = bool(flipped)


# Simple DHT11 mock
class _DHT11:
    def __init__(self, pin):
        self._temperature = 24.5
        self._humidity = 48.0

    @property
    def temperature(self):
        # Slightly vary over time
        return round(self._temperature, 1)

    @property
    def humidity(self):
        return round(self._humidity, 1)


# Simple Serial mock for GPS
class _Serial:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = True
        self._counter = 0

    def readline(self):
        # Return a fake GPGGA NMEA sentence with lat/lon that changes slowly
        self._counter += 1
        lat = 12.3456 + (self._counter % 10) * 0.0001
        lon = 65.4321 - (self._counter % 10) * 0.0001
        line = f"$GPGGA,1,{lat:.6f},0,{lon:.6f},1,08,0.9,545.4,M,46.9,M,,*47\r\n"
        return line.encode('ascii')

    def close(self):
        self.is_open = False


# Simple PyAudio mock
class _PyAudio:
    paInt16 = 8

    class _Stream:
        def __init__(self):
            self._open = True

        def read(self, n, exception_on_overflow=True):
            return b"\x00" * n

        def stop_stream(self):
            pass

        def close(self):
            pass

    def open(self, *args, **kwargs):
        return _PyAudio._Stream()

    def terminate(self):
        pass


def install_mocks(set_flip=False, use_audio=True):
    """Install mock modules into sys.modules for running on non-Pi platforms.

    Args:
        set_flip: If True, set orientation sensor to flipped state.
        use_audio: If False, do not install a PyAudio mock so real microphone/speaker can be used.
    """
    # RPi.GPIO
    gpio_mod = ModuleType('RPi.GPIO')
    gpio = _GPIO()
    # Bind methods/attrs
    gpio_mod.BCM = gpio.BCM
    gpio_mod.OUT = gpio.OUT
    gpio_mod.IN = gpio.IN
    gpio_mod.HIGH = gpio.HIGH
    gpio_mod.LOW = gpio.LOW
    gpio_mod.PUD_DOWN = gpio.PUD_DOWN
    gpio_mod.PUD_UP = gpio.PUD_UP
    gpio_mod.setmode = gpio.setmode
    gpio_mod.setup = gpio.setup
    gpio_mod.output = gpio.output
    gpio_mod.input = gpio.input
    gpio_mod.cleanup = gpio.cleanup
    gpio_mod.set_flip = gpio.set_flip

    sys.modules['RPi'] = ModuleType('RPi')
    sys.modules['RPi.GPIO'] = gpio_mod

    # adafruit_dht
    dht_mod = ModuleType('adafruit_dht')
    dht_mod.DHT11 = _DHT11
    sys.modules['adafruit_dht'] = dht_mod

    # board
    board_mod = ModuleType('board')
    board_mod.D4 = 'D4'
    sys.modules['board'] = board_mod

    # serial
    serial_mod = ModuleType('serial')
    serial_mod.Serial = _Serial
    sys.modules['serial'] = serial_mod

    # pyaudio (optional)
    if use_audio:
        pyaudio_mod = ModuleType('pyaudio')
        pyaudio_mod.PyAudio = _PyAudio
        pyaudio_mod.paInt16 = _PyAudio.paInt16
        sys.modules['pyaudio'] = pyaudio_mod

    # Allow tests to set flip status
    if set_flip:
        gpio.set_flip(True)

    # Expose helper to tests
    sys.modules['dev_mocks'] = ModuleType('dev_mocks')
    sys.modules['dev_mocks'].set_flip = gpio.set_flip
    sys.modules['dev_mocks'].gpio = gpio

    return True
