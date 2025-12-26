# 🔧 PROJECT_SPEC.md - Complete Technical Specification

> **Purpose**: This file contains ALL technical details needed for AI to generate ready-to-use code for the Panda robot project.

---

## 📌 Table of Contents

1. [Hardware Pin Mappings](#1-hardware-pin-mappings)
2. [Arduino Serial Communication Protocol](#2-arduino-serial-communication-protocol)
3. [API Keys & Configuration](#3-api-keys--configuration)
4. [Sensor Thresholds & Parameters](#4-sensor-thresholds--parameters)
5. [Audio System Configuration](#5-audio-system-configuration)
6. [Intent Recognition Patterns](#6-intent-recognition-patterns)
7. [Movement Control Parameters](#7-movement-control-parameters)
8. [Power Specifications](#8-power-specifications)
9. [Python Dependencies](#9-python-dependencies)
10. [System States & Error Codes](#10-system-states--error-codes)
11. [LCD Display Format](#11-lcd-display-format)
12. [Technology Stack Choices](#12-technology-stack-choices)
13. [Threading Architecture](#13-threading-architecture)
14. [Timing & Performance Requirements](#14-timing--performance-requirements)
15. [State Machine Diagram](#15-state-machine-diagram)
16. [Memory & Storage Requirements](#16-memory--storage-requirements)
17. [Network Requirements](#17-network-requirements)
18. [Calibration Procedures](#18-calibration-procedures)
19. [Error Recovery Strategies](#19-error-recovery-strategies)
20. [Logging Configuration](#20-logging-configuration)
21. [Arduino Code](#21-arduino-code)

---

## 1. Hardware Pin Mappings

### Raspberry Pi GPIO Pin Configuration

| Component | Pin Type | GPIO Pin | Physical Pin | Notes |
|-----------|----------|----------|--------------|-------|
| **Ultrasonic Left TRIG** | Output | ⚠️ MISSING | ⚠️ MISSING | |
| **Ultrasonic Left ECHO** | Input | ⚠️ MISSING | ⚠️ MISSING | |
| **Ultrasonic Right TRIG** | Output | ⚠️ MISSING | ⚠️ MISSING | |
| **Ultrasonic Right ECHO** | Input | ⚠️ MISSING | ⚠️ MISSING | |
| **MQ-9 Analog** | ADC/Input | ⚠️ MISSING | ⚠️ MISSING | Requires ADC (MCP3008?) |
| **DHT11 Data** | I/O | ⚠️ MISSING | ⚠️ MISSING | |
| **LED Array** | Output | ⚠️ MISSING | ⚠️ MISSING | Specify all 20 pins or shift register? |
| **Buzzer** | Output | ⚠️ MISSING | ⚠️ MISSING | |
| **Movement Toggle Button** | Input (Pull-up/down?) | ⚠️ MISSING | ⚠️ MISSING | |
| **Help Button** | Input (Pull-up/down?) | ⚠️ MISSING | ⚠️ MISSING | |
| **LCD SDA** | I²C | GPIO 2 | Pin 3 | ✅ Confirmed |
| **LCD SCL** | I²C | GPIO 3 | Pin 5 | ✅ Confirmed |

### Arduino Pin Configuration

| Component | Arduino Pin | Notes |
|-----------|-------------|-------|
| **Motor Left (via L293D)** | ⚠️ MISSING | Which pins on shield? |
| **Motor Right (via L293D)** | ⚠️ MISSING | Which pins on shield? |
| **Camera Servo** | ⚠️ MISSING | PWM pin |
| **Serial to Pi** | RX: 0, TX: 1 | USB connection |

### GPS Module Connection

| GPS Pin | Connected To | Notes |
|---------|--------------|-------|
| VCC | ⚠️ MISSING | 3.3V or 5V? |
| GND | ⚠️ MISSING | |
| TX | ⚠️ MISSING | Which Pi GPIO? |
| RX | ⚠️ MISSING | Which Pi GPIO? |

---

## 2. Arduino Serial Communication Protocol

### Serial Configuration
- **Baud Rate**: ⚠️ MISSING (9600? 115200?)
- **Data Bits**: ⚠️ MISSING (8?)
- **Parity**: ⚠️ MISSING (None?)
- **Stop Bits**: ⚠️ MISSING (1?)

### Commands: Raspberry Pi → Arduino

| Command | Format | Example | Description |
|---------|--------|---------|-------------|
| **Move Forward** | ⚠️ MISSING | `F:200` ? | Speed range? |
| **Move Backward** | ⚠️ MISSING | `B:150` ? | Speed range? |
| **Turn Left** | ⚠️ MISSING | `L:180:500` ? | Speed + duration? |
| **Turn Right** | ⚠️ MISSING | `R:180:500` ? | Speed + duration? |
| **Stop** | ⚠️ MISSING | `S` ? | Immediate stop? |
| **Camera Tilt** | ⚠️ MISSING | `C:90` ? | Angle 0-180? |

### Responses: Arduino → Raspberry Pi

| Response Type | Format | Example | Description |
|---------------|--------|---------|-------------|
| **Acknowledgment** | ⚠️ MISSING | `ACK:F` ? | Command received? |
| **Error** | ⚠️ MISSING | `ERR:01` ? | Error codes? |
| **Status** | ⚠️ MISSING | - | Motor status? Battery? |

### Command Terminator
- **Line Ending**: ⚠️ MISSING (`\n`? `\r\n`? None?)

---

## 3. API Keys & Configuration

### Required API Keys

Create `config/settings.py` with:

```python
# OpenAI API
OPENAI_API_KEY = "⚠️ MISSING"  # Get from: https://platform.openai.com
OPENAI_MODEL = "⚠️ MISSING"     # gpt-4? gpt-3.5-turbo?
OPENAI_MAX_TOKENS = ⚠️ MISSING   # 150? 500?
OPENAI_TEMPERATURE = ⚠️ MISSING  # 0.7?

# Text-to-Speech Service
TTS_SERVICE = "⚠️ MISSING"      # "google"? "elevenlabs"? "pyttsx3"?
TTS_API_KEY = "⚠️ MISSING"      # If required by service
TTS_VOICE = "⚠️ MISSING"        # Which voice?
TTS_SPEED = ⚠️ MISSING           # 1.0?

# Email Alerts (for Help button)
EMAIL_ENABLED = ⚠️ MISSING       # True/False
EMAIL_SENDER = "⚠️ MISSING"     # your-email@gmail.com
EMAIL_PASSWORD = "⚠️ MISSING"   # App password for Gmail
EMAIL_RECIPIENT = "⚠️ MISSING"  # emergency-contact@example.com
SMTP_SERVER = "⚠️ MISSING"      # smtp.gmail.com?
SMTP_PORT = ⚠️ MISSING           # 587? 465?

# Wake Word Detection
WAKEWORD_SERVICE = "⚠️ MISSING"  # "porcupine"? "snowboy"?
WAKEWORD_API_KEY = "⚠️ MISSING"  # If required
WAKEWORD_MODEL_PATH = "⚠️ MISSING"  # Path to .ppn or .pmdl file

# Speech-to-Text
STT_SERVICE = "⚠️ MISSING"       # "google"? "whisper"?
STT_LANGUAGE = "⚠️ MISSING"      # "en-US"? "ar-DZ"?
STT_API_KEY = "⚠️ MISSING"       # If required

# GPS (if using online services)
GPS_ENABLED = ⚠️ MISSING          # True/False
GPS_API_KEY = "⚠️ MISSING"       # If needed for reverse geocoding
```

---

## 4. Sensor Thresholds & Parameters

### Ultrasonic Sensors (HC-SR04)
```python
# Distance thresholds (derived from code)
ULTRASONIC_OBSTACLE_THRESHOLD = 25    # cm (matches core/obstacle_avoidance.OBSTACLE_DISTANCE)
ULTRASONIC_WARNING_THRESHOLD = 30     # cm (matches SAFE_DISTANCE_CM in config/settings.py)
ULTRASONIC_MAX_RANGE = 400           # cm (typical HC-SR04 max)
ULTRASONIC_MEASUREMENT_TIMEOUT = 0.03 # seconds (timeout used in sensors/ultrasonic.py)
ULTRASONIC_POLL_RATE = 10            # Hz (settings.ULTRASONIC_INTERVAL = 0.1 -> 10Hz)
```

### MQ-9 Gas Sensor
```python
# Gas detection (inferred from sensors/mq9.py)
MQ9_DANGER_THRESHOLD = 300       # uses config.GAS_THRESHOLD (config/settings.py)
MQ9_WARMUP_TIME = ⚠️ MISSING     # Not defined in code - please provide if needed
MQ9_SAMPLING_RATE = ⚠️ MISSING   # Not explicitly configured - sensor thread polls periodically
MQ9_USES_ADC = False             # Current implementation uses digital GPIO input (dangerous flag)
MQ9_ADC_CHANNEL = ⚠️ MISSING     # Not applicable for current digital implementation
```

### DHT11 Temperature & Humidity
```python
# Environmental sensor
DHT11_TEMP_MIN = ⚠️ MISSING           # Not specified in repo — please provide operational bounds
DHT11_TEMP_MAX = ⚠️ MISSING
DHT11_HUMIDITY_MIN = ⚠️ MISSING
DHT11_HUMIDITY_MAX = ⚠️ MISSING
DHT11_SAMPLING_INTERVAL = 2.0         # seconds (derived from DHT11Sensor.MIN_READ_INTERVAL in sensors/dht11.py)
```

### Camera
```python
# Vision parameters (inferred from `config/settings.py`)
CAMERA_RESOLUTION = (320, 240)   # (FRAME_WIDTH, FRAME_HEIGHT)
CAMERA_FPS = ⚠️ MISSING           # Not specified in code; please provide desired FPS
CAMERA_DEVICE_INDEX = 0          # CAMERA_SOURCE in settings.py
# Note: DecisionEngine uses FRAME_CENTER_X=160, FRAME_CENTER_Y=120 for (320x240) frames
# and `vision/cascades/pose_landmarker_full.task` is the model used for pose detection.
```

### GPS Module
```python
# GPS settings
GPS_BAUD_RATE = ⚠️ MISSING            # 9600?
GPS_TIMEOUT = ⚠️ MISSING              # seconds (10?)
GPS_UPDATE_RATE = ⚠️ MISSING          # Hz (1?)
```

---

## 5. Audio System Configuration

### Microphone Configuration
```python
# Audio input (inferred from startup._check_microphone)
MIC_DEVICE_INDEX = ⚠️ MISSING    # Not specified; use pyaudio to enumerate
MIC_SAMPLE_RATE = 16000
MIC_CHANNELS = 1
MIC_CHUNK_SIZE = 1024
MIC_FORMAT = pyaudio.paInt16     # requires pyaudio
```

### Wake Word Detection
```python
# Wake word settings
WAKE_WORD = "⚠️ MISSING"              # "Hey Panda"?
WAKE_WORD_SENSITIVITY = ⚠️ MISSING    # 0.0-1.0 (0.5?)
WAKE_WORD_MODEL = "⚠️ MISSING"        # Path to model file
```

### Speech-to-Text
```python
# STT settings
STT_TIMEOUT = ⚠️ MISSING              # seconds (10?)
STT_PHRASE_TIME_LIMIT = ⚠️ MISSING    # seconds (5?)
STT_ENERGY_THRESHOLD = ⚠️ MISSING     # 300? 4000?
STT_DYNAMIC_ENERGY = ⚠️ MISSING       # True/False
```

### Text-to-Speech
```python
# TTS settings
TTS_OUTPUT_DEVICE = ⚠️ MISSING        # default? or specific index?
TTS_CACHE_ENABLED = ⚠️ MISSING        # True/False
TTS_CACHE_PATH = "⚠️ MISSING"         # /path/to/cache?
```

### Session Management
```python
# Conversation settings
SESSION_TIMEOUT = ⚠️ MISSING          # seconds (10?)
SESSION_MAX_COMMANDS = ⚠️ MISSING     # unlimited? or limit?
```

---

## 6. Intent Recognition Patterns

### Local Intent Matching (Before ChatGPT)

```python
# The repository uses a simple keyword-based intent matcher defined in
# `core/speech_engine.py` — see the `INTENTS` dictionary which contains
# phrases used for local intent detection. Current intents include:
# ['greet', 'status', 'temperature', 'time', 'date', 'follow', 'stop',
#  'idle', 'turn_left', 'turn_right', 'thanks', 'goodbye', 'introduce']
# If you want pattern-based matching or additional intents, please provide
# the exact regex patterns or phrases to add.
```


### ChatGPT Fallback Configuration
```python
# When to use ChatGPT
USE_CHATGPT_FOR_UNKNOWN = ⚠️ MISSING    # True/False
CHATGPT_SYSTEM_PROMPT = """⚠️ MISSING"""  # Your exact prompt
```

---

## 7. Movement Control Parameters

### Speed Settings (0-255 scale)
```python
# Motor speeds
# Note: The decision engine uses proportional control and clamps motor outputs.
# Specific motor mapping and PWM ranges must be defined per robot hardware.
SPEED_NORMAL = ⚠️ MISSING      # Define per motor controller
SPEED_SLOW = ⚠️ MISSING
SPEED_TURN = ⚠️ MISSING
SPEED_MIN = ⚠️ MISSING
SPEED_MAX = ⚠️ MISSING
```

### Turn Parameters
```python
# Turning configuration (not explicitly used; motion uses motor commands via actions)
TURN_ANGLE_DEFAULT = ⚠️ MISSING    # degrees
TURN_DURATION_45DEG = ⚠️ MISSING
TURN_DURATION_90DEG = ⚠️ MISSING
TURN_DURATION_180DEG = ⚠️ MISSING
```

### Obstacle Avoidance Behavior
```python
# Avoidance strategy (derived from core/obstacle_avoidance.py)
AVOIDANCE_BACKUP_DISTANCE = 25      # cm (core/obstacle_avoidance.OBSTACLE_DISTANCE)
AVOIDANCE_BACKUP_DURATION = ⚠️ MISSING
AVOIDANCE_RECHECK_DELAY = ⚠️ MISSING
AVOIDANCE_MAX_ATTEMPTS = ⚠️ MISSING
```

### Movement Safety
```python
# Safety parameters (decision control)
MOVEMENT_ENABLED_DEFAULT = ⚠️ MISSING    # Not defined in code
EMERGENCY_STOP_DELAY = 0                  # Immediate stop on emergency
# DecisionEngine control values:
TARGET_DISTANCE_PX = 60
FRAME_CENTER_X = 160
FRAME_CENTER_Y = 120
TURN_GAIN = 0.4
FORWARD_GAIN = 1.2
FORWARD_CLAMP = (-120, 120)
TURN_CLAMP = (-80, 80)
```

---

## 8. Power Specifications

### Current Draw Estimates

| Component | Voltage | Current (Normal) | Current (Peak) | Notes |
|-----------|---------|------------------|----------------|-------|
| Raspberry Pi 4 | 5V | ⚠️ MISSING | ⚠️ MISSING | Typical ~2.5A peak |
| Arduino Uno | 5V | ⚠️ MISSING | ⚠️ MISSING | ~50mA typical |
| Motor Left | 6V | ⚠️ MISSING | ⚠️ MISSING | Stall current? |
| Motor Right | 6V | ⚠️ MISSING | ⚠️ MISSING | Stall current? |
| Camera Servo | 5V | ⚠️ MISSING | ⚠️ MISSING | ~200mA typical |
| USB Camera | 5V | ⚠️ MISSING | ⚠️ MISSING | |
| Ultrasonic (×2) | 5V | ⚠️ MISSING | ⚠️ MISSING | ~15mA each typical |
| DHT11 | 5V | ⚠️ MISSING | ⚠️ MISSING | ~2mA typical |
| MQ-9 | 5V | ⚠️ MISSING | ⚠️ MISSING | ~150mA typical |
| GPS Module | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING | 3.3V or 5V? |
| LED Array (×20) | 5V | ⚠️ MISSING | ⚠️ MISSING | ~20mA each = 400mA total? |
| LCD Display | 5V | ⚠️ MISSING | ⚠️ MISSING | ~50mA typical |
| Buzzer | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING | |

### Power Supply Details
```python
# Raspberry Pi circuit
PI_POWER_SOURCE = "⚠️ MISSING"        # Power bank model/capacity
PI_POWER_CAPACITY = ⚠️ MISSING        # mAh (10000?)
PI_POWER_OUTPUT = ⚠️ MISSING          # A (2.5A? 3A?)

# Motor circuit
MOTOR_POWER_SOURCE = "⚠️ MISSING"     # 4× AA batteries?
MOTOR_VOLTAGE = ⚠️ MISSING            # V (6V nominal?)
MOTOR_CAPACITY = ⚠️ MISSING           # mAh (2500 for AA?)

# Estimated runtime
ESTIMATED_RUNTIME_IDLE = ⚠️ MISSING   # hours
ESTIMATED_RUNTIME_ACTIVE = ⚠️ MISSING # hours
```

---

## 9. Python Dependencies

### Complete requirements.txt

```txt
# ⚠️ Specify exact versions before deployment
# Core runtime
RPi.GPIO
opencv-python
mediapipe
numpy
pyserial
pyaudio
adafruit-circuitpython-dht
adafruit-blinka
pyttsx3
# Optional/dev
opencv-python-headless  # for headless runs/tests
pytest  # for unit tests
```
smbus2==⚠️ MISSING
pyserial==⚠️ MISSING

# Audio Processing
pyaudio==⚠️ MISSING
SpeechRecognition==⚠️ MISSING
# ⚠️ MISSING - Which TTS library? pyttsx3? gTTS? other?
# ⚠️ MISSING - Which wake word library? pvporcupine? snowboy? other?

# Computer Vision
opencv-python==⚠️ MISSING
# ⚠️ MISSING - picamera2 if using Pi Camera? Or USB camera only?

# AI/ML
openai==⚠️ MISSING
numpy==⚠️ MISSING

# Sensors
# ⚠️ MISSING - Which DHT library? Adafruit-DHT? adafruit-circuitpython-dht?
# ⚠️ MISSING - GPS library? gpsd? pynmea2?
# ⚠️ MISSING - ADC library for MQ-9? adafruit-mcp3008?

# Scheduling
schedule==⚠️ MISSING
python-dateutil==⚠️ MISSING

# Communication
requests==⚠️ MISSING

# Display
# ⚠️ MISSING - Which LCD library? RPLCD? adafruit-circuitpython-charlcd?

# Utilities
python-dotenv==⚠️ MISSING
```

### System-Level Dependencies
```bash
# ⚠️ MISSING - List apt packages needed
# Example: sudo apt-get install -y portaudio19-dev python3-dev
```

---

## 10. System States & Error Codes

### Robot States Enumeration
```python
class RobotState(Enum):
    BOOT = "⚠️ MISSING"           # Initial startup?
    IDLE = "⚠️ MISSING"           # Waiting for wake word?
    LISTENING = "⚠️ MISSING"      # Recording audio?
    PROCESSING = "⚠️ MISSING"     # Analyzing command?
    SPEAKING = "⚠️ MISSING"       # Playing TTS?
    MOVING = "⚠️ MISSING"         # Motors active?
    EMERGENCY_STOP = "⚠️ MISSING" # Gas detected or critical error?
    SENSOR_FAILURE = "⚠️ MISSING" # Degraded mode?
    # ⚠️ MISSING - Any other states?
```

### Error Codes
| Code | Name | Meaning | Recovery Action |
|------|------|---------|-----------------|
| E01 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |
| E02 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |
| E03 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |
| E04 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |
| E05 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |

### Warning Codes
| Code | Name | Meaning | Action |
|------|------|---------|--------|
| W01 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |
| W02 | ⚠️ MISSING | ⚠️ MISSING | ⚠️ MISSING |

---

## 11. LCD Display Format

### Display Specifications
```python
LCD_COLUMNS = 16                # ✅ Confirmed
LCD_ROWS = 2                    # ✅ Confirmed
LCD_I2C_ADDRESS = ⚠️ MISSING    # 0x27? 0x3F? Check with i2cdetect
```

### Display Messages Format

```python
# ⚠️ MISSING - Specify exact format for each state

# Example formats (need confirmation):
DISPLAY_IDLE = [
    "⚠️ MISSING      ",  # Line 1 (16 chars)
    "⚠️ MISSING      "   # Line 2 (16 chars)
]

DISPLAY_LISTENING = [
    "⚠️ MISSING      ",
    "⚠️ MISSING      "
]

DISPLAY_MOVING_FORWARD = [
    "⚠️ MISSING      ",
    "⚠️ MISSING      "
]

DISPLAY_EMERGENCY = [
    "⚠️ MISSING      ",
    "⚠️ MISSING      "
]

# ⚠️ MISSING - How to display temperature/humidity?
# ⚠️ MISSING - How to display time?
# ⚠️ MISSING - How to display alarms?
```

---

## 12. Technology Stack Choices

### ⚠️ CRITICAL: Specify Exact Libraries/Services Used

```python
# Wake Word Detection
WAKEWORD_LIBRARY = "⚠️ MISSING"  # "porcupine"? "snowboy"? "precise"?

# Speech-to-Text
STT_ENGINE = "⚠️ MISSING"        # "google"? "whisper"? "sphinx"?

# Text-to-Speech
TTS_ENGINE = "⚠️ MISSING"        # "gtts"? "pyttsx3"? "elevenlabs"?

# Computer Vision
CV_LIBRARY = "⚠️ MISSING"        # "opencv"? "mediapipe"?

# Sensors
DHT_LIBRARY = "⚠️ MISSING"       # "Adafruit_DHT"? "adafruit-circuitpython-dht"?
GPS_LIBRARY = "⚠️ MISSING"       # "gpsd"? "pynmea2"?
LCD_LIBRARY = "⚠️ MISSING"       # "RPLCD"? "adafruit-charlcd"?

# ChatGPT
OPENAI_MODEL = "⚠️ MISSING"      # "gpt-4"? "gpt-3.5-turbo"?
```

---

## 13. Threading Architecture

### Thread Structure (inferred from code)
```python
# Threads observed in the codebase:
# - Main thread: starts system, runs the DecisionEngine.update() loop (control loop)
# - Vision thread: `vision.VisionEngine` runs as a daemon Thread and sets a readiness Event; exposes `get_target()` guarded by an internal Lock
# - Ultrasonic sensor thread(s): `sensors.ultrasonic.UltrasonicArray` starts a background thread to poll distances and update `latest_data`
# - DHT11 thread: `sensors.dht11.DHT11Sensor` runs a thread to periodically update temperature/humidity
# - MQ9 thread: `sensors.mq9.MQ9Sensor` runs a thread to update gas status
# - GPS thread: `sensors.gps.GPSModule` runs a thread to parse serial NMEA lines and update `latest_data`
# - Optional scheduler thread: code references `startup` scheduler interval in settings and a scheduler module exists (startup/scheduler.py) which may run periodic jobs
```

### Thread Communication (observed patterns)
```python
# Current code uses shared objects and simple APIs rather than a central queue system:
# - Sensors: each sensor class exposes a thread-safe `read()` that returns the latest snapshot dict
# - Vision: exposes `get_target()` and protects updates with a threading.Lock
# - Decision loop calls sensor.read() and vision.get_target() synchronously in the main loop
# - Actions are called directly from the DecisionEngine (no command queue)
```

### Thread Safety Rules (recommendations / findings)
- Vision already uses an internal `Lock` to protect `target_center` / `target_width` access — keep this pattern for other shared state.
- Sensor `read()` methods return immutable snapshots/dicts (best-effort) — prefer that over shared mutable state.
- Motor and actuator calls should be funneled through a single `actions` module and consider adding a small mutex or command queue if concurrent callers are possible.
- Use Events for system-level flags (e.g., `shutdown_event`, `emergency_stop_event`).

---


---

## 14. Timing & Performance Requirements

### Response Time Targets (needs your confirmation)
| Action | Observed / Inferred | Note |
|--------|---------------------|------|
| Wake word → response | NOT IMPLEMENTED | Wake-word/STT not implemented in code; please provide targets if required |
| STT processing | NOT IMPLEMENTED | STT integration is not present — add service & targets |
| Emergency stop (gas) | Immediate (reactive) | MQ9 is read by a background thread; DecisionEngine prioritizes ALARM state — provide millisecond target if you need a SLA |
| Obstacle detect → stop | <= 1 control loop tick (50 ms) | Decision loop runs at ~20Hz (time.sleep(0.05)) so response to obstacle is within that tick; specify stricter targets if needed |
| Command → motor action | <= 50 ms (decision tick) | As above, motor commands are applied inside DecisionEngine cycle |
| Display update | 0.5s refresh (config LCD_INTERVAL) | `settings.LCD_INTERVAL = 0.5` is present

### Loop Frequencies (inferred from code)
```python
SENSOR_POLL_RATE = 10           # Ultrasonic: settings.ULTRASONIC_INTERVAL = 0.1 -> 10Hz
DECISION_ENGINE_RATE = 20       # Decision loop uses time.sleep(0.05) -> 20Hz
ULTRASONIC_MEASURE_RATE = 10    # See ultrasonic sensor thread and settings
LCD_REFRESH_RATE = 2           # settings.LCD_INTERVAL = 0.5 -> 2Hz
SCHEDULER_RATE = 1/60          # settings.SCHEDULER_INTERVAL = 60s
```

**Ask:** If you require hard real-time guarantees or determinism, please specify exact timing SLAs (max latency) for wake-word, STT, obstacle stop, and emergency alarm handling so I can add watchdogs and tighter mechanisms.

---
---

## 15. State Machine Diagram

### State Transitions (inferred from `core/decision_engine.py` and `core/speech_engine.py`)
```
BOOT → IDLE (automatic after initialization)
IDLE → MOVE (when a 'follow' intent is detected OR when vision target is present and commanded to follow)
MOVE → SEARCH (if vision target is lost for > VISION_LOST_TIMEOUT)
SEARCH → MOVE (when vision reacquires target)
* → ALARM (immediate on MQ9 dangerous_CO == True)
ALARM → (manual / system reset) (requires a safe reset action)
IDLE → INTERACT (on 'greet' or 'status' intents)
INTERACT → IDLE (after interaction or when 'idle' intent is processed)
IDLE ↔ SAFETY_STOP (entered on safety triggers; recovery unspecified in code)
```

### State Constraints / Rules (observed)
- ALARM state is highest priority: when set, decision engine rings alarm and stops motors; voice commands are ignored while in ALARM.
- Obstacle avoidance is checked before movement; if `obstacle_avoidance.should_avoid()` (or `avoid()`) triggers, it performs avoidance maneuvers and preempts normal MOVE behavior.
- The robot will not enter MOVE state if `vision` is not available — DecisionEngine warns and refuses to move.

**Ask:** Define recovery behavior from ALARM and SAFETY_STOP (e.g., manual confirmation via button, automatic re-check after X seconds, or remote override). Also confirm whether the robot may accept non-critical voice commands while moving (currently not explicitly blocked).

---
---

## 16. Memory & Storage Requirements

### Observations
- The code loads OpenCV and MediaPipe models which can be memory-heavy at runtime. The exact memory footprint depends on model sizes and whether hardware acceleration is used.

### Required from you (cannot be inferred from code)
Please provide the deployment target (Raspberry Pi model: Pi 3, Pi 4 2GB/4GB/8GB) and any SD card sizing or storage constraints. Once you provide the target hardware, I will add recommended values for:
- CODE_SIZE, LOG_SIZE_DAILY, AUDIO_CACHE_SIZE, MINIMUM_FREE_SPACE
- PYTHON_BASELINE, OPENCV_LOADED, AUDIO_BUFFERS, SENSOR_DATA, RECOMMENDED_FREE_RAM
- SD_CARD_MIN_SIZE and SD_CARD_CLASS

---


---

## 17. Network Requirements

### Internet Connectivity

```python
# Bandwidth per interaction
STT_REQUEST_SIZE = ⚠️ MISSING       # KB (~100?)
CHATGPT_REQUEST_SIZE = ⚠️ MISSING   # KB (~10?)
CHATGPT_RESPONSE_SIZE = ⚠️ MISSING  # KB (~5?)
TTS_REQUEST_SIZE = ⚠️ MISSING       # KB (~50?)

AVERAGE_INTERACTION = ⚠️ MISSING    # KB (~200?)
```

### Fallback Behavior
⚠️ MISSING - Specify offline mode behavior:
- What works offline?
- What degrades?
- How to detect connection loss?
- Reconnection strategy?

### WiFi Configuration
⚠️ MISSING - Provide WiFi setup instructions:
- How to configure on first boot?
- Multiple network support?
- Auto-reconnect settings?

---

## 18. Calibration Procedures

### Ultrasonic Sensor Calibration
⚠️ MISSING - Specify calibration procedure:
- How to verify accuracy?
- How to adjust offsets?
- Frequency of recalibration?

### MQ-9 Gas Sensor Calibration
⚠️ MISSING - Specify calibration procedure:
- Warm-up time required?
- Baseline measurement in clean air?
- How to calculate danger threshold?
- Frequency of recalibration?

### Motor Speed Calibration
⚠️ MISSING - Specify calibration procedure:
- How to check if motors are balanced?
- How to measure actual speed?
- How to adjust for differences?
- Compensation factors storage?

### Camera Calibration
⚠️ MISSING - If using for person detection:
- Field of view adjustment?
- Focus settings?
- Lighting compensation?

---

## 19. Error Recovery Strategies

### Automatic Recovery Procedures

#### Sensor Failures
```python
# ⚠️ MISSING - Specify recovery strategy for each sensor

# Example (needs confirmation):
def on_ultrasonic_failure(sensor_id):
    """
    ⚠️ MISSING - Specify:
    1. How many retries?
    2. Retry delay?
    3. Fallback behavior?
    4. User notification method?
    5. When to give up?
    """
    pass

def on_dht11_timeout():
    """
    ⚠️ MISSING - Specify:
    1. Use last known value?
    2. Show error on display?
    3. How many failures before disable?
    """
    pass

def on_camera_error():
    """
    ⚠️ MISSING - Specify:
    1. Disable vision features?
    2. Continue operation?
    3. Retry or permanent disable?
    """
    pass

def on_mq9_failure():
    """
    ⚠️ MISSING - Critical sensor:
    1. Assume safe or dangerous?
    2. Emergency stop?
    3. Alert user?
    """
    pass
```

#### Communication Failures
```python
# ⚠️ MISSING - Specify recovery procedures

def on_arduino_timeout():
    """
    ⚠️ MISSING - Specify:
    1. Reconnection attempts?
    2. Delay between attempts?
    3. Emergency stop if failed?
    4. Manual restart required?
    """
    pass

def on_wifi_disconnect():
    """
    ⚠️ MISSING - Specify:
    1. Switch to offline mode automatically?
    2. Queue API-dependent commands?
    3. Retry interval?
    4. User notification?
    """
    pass

def on_api_error(service):
    """
    ⚠️ MISSING - Specify per service:
    - OpenAI/ChatGPT: Fallback behavior?
    - STT: Local alternative?
    - TTS: Cached responses?
    """
    pass
```

---

## 20. Logging Configuration

### Log Files Structure
```python
# ⚠️ MISSING - Specify logging strategy

LOGS_DIR = "⚠️ MISSING"  # /home/pi/PI_BRAIN/logs/ ?

# Separate log files or single file?
LOG_FILES = {
    "main": "⚠️ MISSING",      # panda_main.log?
    "sensors": "⚠️ MISSING",   # panda_sensors.log?
    "movement": "⚠️ MISSING",  # panda_movement.log?
    "errors": "⚠️ MISSING",    # panda_errors.log?
    "audio": "⚠️ MISSING"      # panda_audio.log?
}
```

### Log Entry Format
⚠️ MISSING - Specify format:
```
Example: [2025-12-26 14:32:15.123] [LEVEL] [MODULE] Message
Or different format?
```

### Log Levels
⚠️ MISSING - When to use each level:
- DEBUG: ?
- INFO: ?
- WARNING: ?
- ERROR: ?
- CRITICAL: ?

### Log Rotation
⚠️ MISSING - Specify:
- Maximum log file size?
- Number of backup files?
- Compression of old logs?
- Auto-delete after X days?

---

## 21. Arduino Code

### Complete Arduino Sketch

⚠️ MISSING - Provide the complete `motor_controller.ino` code

The Arduino code should include:
1. Serial communication setup
2. Command parser
3. Motor control logic (using L293D)
4. Servo control for camera
5. Acknowledgment/error responses
6. Watchdog/timeout handling

**Critical:** Without this code, the Raspberry Pi cannot communicate with Arduino correctly.

---

## 22. Implementation Guidelines

### Code Style & Standards

```python
# Programming Language
PYTHON_VERSION = "⚠️ MISSING"  # 3.9+? 3.11?

# Code Formatting
CODE_FORMATTER = "⚠️ MISSING"  # Black? autopep8? None?
LINE_LENGTH = ⚠️ MISSING        # 79? 88? 100?
USE_TYPE_HINTS = ⚠️ MISSING     # True/False

# Naming Conventions
# ⚠️ MISSING - Confirm standard:
# - Functions/variables: snake_case?
# - Classes: PascalCase?
# - Constants: UPPER_SNAKE_CASE?
# - Private methods: _leading_underscore?

# Docstring Style
DOCSTRING_FORMAT = "⚠️ MISSING"  # Google? NumPy? reStructuredText?

# Example (needs confirmation):
"""
def function_name(param1, param2):
    '''
    Brief description.
    
    Args:
        param1 (type): Description
        param2 (type): Description
    
    Returns:
        type: Description
    
    Raises:
        ExceptionType: When this happens
    '''
    pass
"""
```

### Architecture Patterns

⚠️ MISSING - Specify architectural decisions:

```python
# Hardware Abstraction
# - One class per hardware component?
# - Singleton pattern for hardware managers?
# - Factory pattern for sensors?

# Code Organization
# - Functional programming or OOP?
# - Where does each logic piece belong?

# Example (needs confirmation):
"""
sensors/
├── sensor.py           # SensorManager class (aggregator)
├── ultrasonic.py       # UltrasonicSensor class
├── dht11.py           # DHT11Sensor class
└── base_sensor.py     # BaseSensor abstract class?
"""

# Communication Between Modules
# - Direct function calls?
# - Event-driven (pub/sub)?
# - Message queue system?
# - Shared state objects?

# State Management
# - Single StateManager class?
# - Distributed state?
# - How to ensure thread safety?

# Configuration Access
# - Import settings directly?
# - Pass config objects?
# - Dependency injection?
```

### Error Handling Philosophy

⚠️ MISSING - Define error handling strategy:

```python
# General Approach
# - Try/except everywhere or fail-fast?
# - Catch specific exceptions or broad Exception?
# - Re-raise or handle locally?

# Retry Logic
RETRY_ATTEMPTS = ⚠️ MISSING      # 3?
RETRY_DELAY = ⚠️ MISSING         # seconds (1?)
RETRY_BACKOFF = ⚠️ MISSING       # Exponential? Linear?

# Critical vs Non-Critical Failures
# ⚠️ MISSING - Define behavior:
# Critical (ultrasonic, MQ-9): Emergency stop?
# Non-critical (DHT11, camera): Continue?

# User Notification
# - Display error on LCD?
# - Voice announcement?
# - Log only?
# - Email alert?
```

### Data Structures & Formats

⚠️ MISSING - Define standard data structures:

```python
# Sensor Data Format
# Option 1: Dictionary
sensor_data = {
    'ultrasonic_left': float,
    'ultrasonic_right': float,
    'temperature': float,
    'humidity': float,
    'gas_level': int,
    'timestamp': datetime
}

# Option 2: Dataclass (Python 3.7+)
from dataclasses import dataclass

@dataclass
class SensorData:
    ultrasonic_left: float
    ultrasonic_right: float
    temperature: float
    humidity: float
    gas_level: int
    timestamp: datetime

# Option 3: NamedTuple
from typing import NamedTuple

class SensorData(NamedTuple):
    ultrasonic_left: float
    ultrasonic_right: float
    temperature: float
    humidity: float
    gas_level: int
    timestamp: datetime

# ⚠️ MISSING - Which format to use?

# Command Format
# ⚠️ MISSING - Define structure for internal commands:
"""
{
    'type': str,           # 'move', 'speak', 'alarm'
    'parameters': dict,    # command-specific
    'priority': int,       # 0=normal, 1=high, 2=emergency
    'timestamp': datetime
}
"""
```

### Thread Safety Rules

⚠️ MISSING - Define threading rules:

```python
# Shared Resources Access
# - Which data structures are shared?
# - Queue.Queue for thread-safe passing?
# - threading.Lock for critical sections?
# - threading.Event for flags?

# Example (needs confirmation):
"""
Sensor data:
- Producer: sensor_polling_thread (writes)
- Consumer: decision_engine_loop (reads)
- Structure: Queue.Queue(maxsize=10)

Motor commands:
- Multiple threads may send commands
- Use threading.Lock on serial port
- Queue commands if port busy

State changes:
- Use threading.Lock when modifying state
- Read-only access without lock?
"""

# Deadlock Prevention
# ⚠️ MISSING - Rules to prevent deadlocks:
# - Always acquire locks in same order?
# - Use timeout on lock acquisition?
# - Avoid nested locks?
```

### Testing Strategy

⚠️ MISSING - Define testing approach:

```python
# Running Without Hardware
SIMULATION_MODE = ⚠️ MISSING  # Environment variable? Config?

# Mock Objects
# - Mock GPIO when not available?
# - Mock sensors with random/fixed data?
# - Mock Arduino serial?

# Example (needs confirmation):
"""
try:
    import RPi.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except ImportError:
    from mocks.gpio_mock import GPIO
    HARDWARE_AVAILABLE = False
    print("Running in simulation mode")
"""

# Unit Tests
# - Test each module independently?
# - Use pytest? unittest?
# - Mock hardware dependencies?

# Integration Tests
# - Test full workflow?
# - Require hardware?
# - How to automate?
```

### Boot Sequence & Initialization

⚠️ MISSING - Define exact startup procedure:

```python
# Startup Order (example, needs confirmation):
"""
1. Initialize logging system (FIRST!)
2. Load configuration from settings.py
3. Check for required API keys
4. Initialize GPIO (with error handling)
5. Initialize hardware managers:
   - LCD display (show "Starting...")
   - Sensors (parallel initialization?)
   - Arduino serial connection
   - Audio system
6. Start background threads:
   - Sensor polling thread (daemon)
   - Audio listening thread (daemon)
   - Display update thread (daemon)
   - Scheduler thread (daemon)
7. Run system self-check
8. Display "Ready" message
9. Enter main decision loop

On any initialization failure:
- Log error details
- Display error on LCD
- Decide: Continue without or abort?
"""
```

### Shutdown Procedure

⚠️ MISSING - Define graceful shutdown:

```python
# Shutdown Steps (example, needs confirmation):
"""
1. Set global shutdown flag
2. Stop accepting new commands
3. Complete current operation (timeout?)
4. Stop all motors
5. Stop background threads (join with timeout)
6. Close serial connections
7. Cleanup GPIO
8. Flush logs
9. Display "Shutdown" message
10. Exit
"""

# Signal Handling
# - Catch SIGINT (Ctrl+C)?
# - Catch SIGTERM (systemd stop)?
# - Graceful vs immediate shutdown?
```

### File Organization Principles

⚠️ MISSING - Clarify organization rules:

```python
# File Size Limits
MAX_LINES_PER_FILE = ⚠️ MISSING  # 500? 1000?

# Module Responsibilities
# - One responsibility per file?
# - Related functions grouped?
# - How to split large modules?

# Import Rules
# - Absolute imports only?
# - Relative imports allowed?
# - Avoid circular imports (how?)

# Directory Structure Rules
# - Group by feature or by type?
# - Where do utility functions go?
# - Where do constants go?
```

---

## 23. Default Behaviors & Assumptions

### Startup Defaults

⚠️ MISSING - Specify initial states:

```python
# On System Boot
INITIAL_STATE = "⚠️ MISSING"           # "BOOT"? "IDLE"?
MOVEMENT_ENABLED_DEFAULT = ⚠️ MISSING  # True/False
VOLUME_DEFAULT = ⚠️ MISSING            # 0-100 (70?)
LED_BRIGHTNESS_DEFAULT = ⚠️ MISSING    # 0-100 (100?)
CAMERA_SERVO_DEFAULT = ⚠️ MISSING      # degrees (90=center?)

# Display Messages
BOOT_MESSAGE_LINE1 = "⚠️ MISSING"      # "Starting..."?
BOOT_MESSAGE_LINE2 = "⚠️ MISSING"      # "Please wait"?
READY_MESSAGE_LINE1 = "⚠️ MISSING"     # "Panda Ready"?
READY_MESSAGE_LINE2 = "⚠️ MISSING"     # "Say Hey Panda"?
```

### Sensor Failure Behaviors

⚠️ MISSING - Define fallback behavior for each sensor:

```python
# Ultrasonic Sensors
ON_ULTRASONIC_FAILURE = "⚠️ MISSING"
# Options:
# - "STOP": Emergency stop
# - "SLOW": Reduce speed to 50%
# - "LAST": Use last known reading
# - "SINGLE": Continue with one sensor only

# DHT11 Temperature/Humidity
ON_DHT11_FAILURE = "⚠️ MISSING"
# Options:
# - "IGNORE": Don't show temp/humidity
# - "DISPLAY_ERROR": Show "---" on LCD
# - "LAST": Use last known value

# MQ-9 Gas Sensor
ON_MQ9_FAILURE = "⚠️ MISSING"
# Options:
# - "ASSUME_SAFE": Continue normally (risky!)
# - "EMERGENCY": Trigger emergency stop (safe)
# - "DISABLE": Disable gas monitoring

# Camera
ON_CAMERA_FAILURE = "⚠️ MISSING"
# Options:
# - "DISABLE_VISION": Continue without vision
# - "RETRY": Keep trying to reconnect
# - "ALERT": Alert user but continue

# GPS Module
ON_GPS_FAILURE = "⚠️ MISSING"
# Options:
# - "SKIP": Send emergency alert without location
# - "RETRY": Wait for GPS fix (timeout?)
# - "LAST": Use last known location
```

### Network Failure Behaviors

⚠️ MISSING - Define offline mode:

```python
# Internet Connection Lost
ON_WIFI_DISCONNECT = "⚠️ MISSING"
# - Switch to offline mode automatically?
# - Show warning on LCD?
# - Queue API-dependent commands?
# - Auto-retry connection interval?

# Offline Mode Capabilities
OFFLINE_STT = "⚠️ MISSING"        # Use pyttsx3? Sphinx? Disable?
OFFLINE_TTS = "⚠️ MISSING"        # Use pyttsx3? Cached audio?
OFFLINE_CHATGPT = "⚠️ MISSING"    # Local responses? "I'm offline" message?

# Reconnection Strategy
WIFI_RETRY_INTERVAL = ⚠️ MISSING  # seconds (30?)
WIFI_RETRY_MAX = ⚠️ MISSING       # attempts (infinite?)
```

### Power Management

⚠️ MISSING - Define low power behaviors:

```python
# If Battery Level Detectable
LOW_BATTERY_THRESHOLD = ⚠️ MISSING    # % (20?)
CRITICAL_BATTERY_THRESHOLD = ⚠️ MISSING  # % (10?)

# Low Battery Actions
ON_LOW_BATTERY = [
    "⚠️ MISSING",  # Reduce LED brightness?
    "⚠️ MISSING",  # Disable camera?
    "⚠️ MISSING",  # Reduce movement speed?
    "⚠️ MISSING"   # Voice alert?
]

# Critical Battery Actions
ON_CRITICAL_BATTERY = [
    "⚠️ MISSING",  # Emergency shutdown?
    "⚠️ MISSING",  # Save state?
    "⚠️ MISSING"   # Alert user?
]
```

### Unknown Command Handling

⚠️ MISSING - Define response to unrecognized commands:

```python
# When Intent Not Recognized
UNKNOWN_COMMAND_RESPONSE = "⚠️ MISSING"
# Example: "I didn't understand. Try 'set alarm' or 'move forward'"

# Action After Unknown Command
UNKNOWN_COMMAND_ACTION = "⚠️ MISSING"
# Options:
# - "PROMPT": Ask user to repeat
# - "CONTINUE": Do nothing, keep listening
# - "LOG": Log for later training
# - "CHATGPT": Always fallback to ChatGPT
```

### Timeout Behaviors

⚠️ MISSING - Define timeout handling:

```python
# Wake Word Detection
WAKE_WORD_TIMEOUT = ⚠️ MISSING    # None (always listening)?

# Listening Session
LISTENING_TIMEOUT = ⚠️ MISSING    # seconds (10?)
LISTENING_SILENCE_THRESHOLD = ⚠️ MISSING  # seconds of silence (2?)

# Movement Operations
MOVEMENT_TIMEOUT = ⚠️ MISSING     # None (manual stop only)?

# TTS Playback
TTS_TIMEOUT = ⚠️ MISSING          # Wait for completion? Timeout?

# API Calls
API_TIMEOUT = ⚠️ MISSING          # seconds (10?)
```

### Conflict Resolution Rules

⚠️ MISSING - Define priority system:

```python
# Command Priority Hierarchy
# Example (needs confirmation):
PRIORITY_ORDER = [
    "⚠️ MISSING",  # 1. Emergency stop (gas detection)
    "⚠️ MISSING",  # 2. Manual stop button
    "⚠️ MISSING",  # 3. Obstacle avoidance
    "⚠️ MISSING",  # 4. User voice command
    "⚠️ MISSING"   # 5. Scheduled tasks
]

# Interrupt Rules
# - Can new command interrupt current movement?
# - Can new command interrupt current speech?
# - Can alarm interrupt movement?

# Multi-Command Handling
# ⚠️ MISSING - If user says "turn left then go forward":
# - Parse and execute sequentially?
# - Execute only first command?
# - Ask for clarification?
```

### Session Management

⚠️ MISSING - Define session behavior:

```python
# Multi-Command Sessions
ALLOW_MULTI_COMMAND = ⚠️ MISSING  # True/False
SESSION_MAX_COMMANDS = ⚠️ MISSING  # unlimited (-1) or limit (5?)

# Session End Conditions
SESSION_ENDS_ON = [
    "⚠️ MISSING",  # Timeout?
    "⚠️ MISSING",  # "Thank you" or "goodbye"?
    "⚠️ MISSING"   # Max commands reached?
]

# Between Commands in Session
WAIT_FOR_NEXT_COMMAND = ⚠️ MISSING  # seconds (5?)
PROMPT_NEXT_COMMAND = ⚠️ MISSING    # "Anything else?" (True/False)
```

---

## 24. Working Code Examples

### Example 1: Reading Ultrasonic Sensor

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of ultrasonic distance measurement.
Include:
- GPIO setup
- Trigger pulse generation
- Echo timing
- Distance calculation
- Error handling
- Timeout handling
"""

import RPi.GPIO as GPIO
import time

def measure_distance(trig_pin, echo_pin, timeout=0.05):
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Sending 10μs trigger pulse
    - Measuring echo pulse width
    - Calculating distance (speed of sound = 34300 cm/s)
    - Timeout if no response
    - Invalid readings (< 2cm or > 400cm)
    """
    pass
```

### Example 2: Arduino Serial Communication

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of Arduino communication.
Include:
- Serial port initialization
- Sending commands
- Receiving acknowledgments
- Error handling
- Timeout handling
- Reconnection logic
"""

import serial
import time

def send_motor_command(ser, command, wait_ack=True, timeout=1.0):
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Sending command with proper terminator
    - Waiting for ACK response
    - Parsing ERR responses
    - Timeout if no response
    - Serial port errors
    """
    pass
```

### Example 3: Thread-Safe State Management

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of thread-safe state manager.
Include:
- State enumeration
- Thread-safe getters/setters
- State change logging
- State transition validation
"""

import threading
from enum import Enum

class RobotState(Enum):
    # ⚠️ MISSING - Define all states
    pass

class StateManager:
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Thread-safe state access
    - State change validation
    - State history tracking (optional)
    - Event notifications on state change (optional)
    """
    pass
```

### Example 4: Sensor Polling Thread

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of sensor polling thread.
Include:
- Continuous sensor reading
- Queue management
- Error handling per sensor
- Graceful shutdown
"""

import threading
import queue
import time

def sensor_polling_thread(sensor_queue, stop_event):
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Reading all sensors
    - Handling individual sensor failures
    - Putting data in queue (with overflow handling)
    - Respecting stop_event
    - Cleanup on exit
    """
    pass
```

### Example 5: Intent Recognition

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of local intent matching.
Include:
- Regex pattern matching
- Parameter extraction
- Confidence scoring (optional)
- Fallback to ChatGPT
"""

import re

def recognize_intent(text):
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Matching against all intent patterns
    - Extracting parameters (time, direction, etc.)
    - Returning intent + parameters
    - Returning None if no match (trigger ChatGPT)
    """
    pass
```

### Example 6: Obstacle Avoidance Logic

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of obstacle avoidance.
Include:
- Distance checking
- Direction decision
- Turn execution
- Re-checking after turn
"""

def check_and_avoid_obstacles(left_distance, right_distance):
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Both sensors clear → continue forward
    - Left blocked → turn right
    - Right blocked → turn left
    - Both blocked → backup then turn
    - Invalid sensor readings
    """
    pass
```

### Example 7: Emergency Stop Handler

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of emergency stop.
Include:
- Immediate motor stop
- Alert generation
- State change
- Recovery procedure
"""

def trigger_emergency_stop(reason):
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Stopping all motors immediately
    - Setting emergency state
    - Buzzer activation
    - Voice/LCD alert
    - Logging
    - Preventing further movement
    """
    pass
```

### Example 8: Configuration Loading

⚠️ MISSING - Provide complete, tested code:

```python
"""
Complete implementation of configuration management.
Include:
- Loading from settings.py
- Environment variable overrides
- Validation
- Default values
"""

def load_configuration():
    """
    ⚠️ MISSING - Complete this implementation
    
    Should handle:
    - Importing settings.py
    - Checking for required values
    - Validating types/ranges
    - Providing sensible defaults
    - Environment variable overrides
    - Raising errors for missing critical config
    """
    pass
```

---

## 25. Testing & Validation Checklist

### Pre-Competition Testing Protocol

⚠️ MISSING - Create detailed test procedures:

#### Hardware Tests (Estimated: 30 minutes)
```markdown
[ ] Power System
    [ ] Raspberry Pi boots in < 60 seconds
    [ ] Arduino connects via USB
    [ ] Battery voltage: ⚠️ MISSING V minimum
    [ ] Power bank capacity test: ⚠️ MISSING minutes runtime
    
[ ] Motors
    [ ] Left motor responds to forward command
    [ ] Right motor responds to forward command
    [ ] Both motors run at same speed (within ⚠️ MISSING %)
    [ ] Backward movement works
    [ ] Turns execute correctly
    
[ ] Sensors (Connectivity)
    [ ] Ultrasonic left returns valid readings
    [ ] Ultrasonic right returns valid readings
    [ ] DHT11 returns temperature/humidity
    [ ] MQ-9 returns analog value
    [ ] GPS gets fix (outdoor test)
    [ ] Camera captures image
    
[ ] Display & Feedback
    [ ] LCD shows boot message
    [ ] LCD updates on command
    [ ] All 20 LEDs illuminate
    [ ] Buzzer produces sound
    [ ] Speaker plays audio
    
[ ] Input Devices
    [ ] Microphone detected by system
    [ ] Movement toggle button works
    [ ] Help button triggers alert
```

#### Software Tests (Estimated: 20 minutes)
```markdown
[ ] Audio Pipeline
    [ ] Wake word detection: ⚠️ MISSING success rate target?
    [ ] Speech-to-text accuracy: ⚠️ MISSING % target?
    [ ] Intent recognition (all built-in commands)
    [ ] ChatGPT fallback responds
    [ ] TTS output clear and understandable
    
[ ] Movement Control
    [ ] Forward movement smooth
    [ ] Turns accurate (⚠️ MISSING degree tolerance?)
    [ ] Stop command immediate (< ⚠️ MISSING ms?)
    [ ] Movement toggle disables motors
    
[ ] Safety Systems
    [ ] Obstacle detection at ⚠️ MISSING cm
    [ ] Obstacle avoidance executes correctly
    [ ] Gas sensor triggers emergency stop
    [ ] Emergency stop locks movement
    [ ] Help button sends email with GPS
    
[ ] State Management
    [ ] State transitions work correctly
    [ ] No race conditions in ⚠️ MISSING minute stress test
    [ ] System recovers from sensor failures
```

#### Integration Tests (Estimated: 30 minutes)
```markdown
[ ] End-to-End Workflows
    [ ] Wake → Command → Execute → Response (< ⚠️ MISSING seconds total)
    [ ] Multi-command session works
    [ ] Alarm setting and triggering
    [ ] Temperature query and response
    
[ ] Continuous Operation
    [ ] Run for ⚠️ MISSING minutes without crash
    [ ] Memory usage stable (no leaks)
    [ ] CPU usage < ⚠️ MISSING % average
    [ ] Log files created correctly
    
[ ] Error Handling
    [ ] WiFi disconnect handled gracefully
    [ ] Sensor failure handled gracefully
    [ ] Arduino disconnect handled gracefully
    [ ] Invalid commands handled gracefully
    
[ ] Performance
    [ ] Response time: wake to action < ⚠️ MISSING seconds
    [ ] CPU usage < ⚠️ MISSING %
    [ ] RAM usage < ⚠️ MISSING GB
    [ ] No dropped sensor readings in ⚠️ MISSING minute test
```

### Competition Demonstration Scenarios

⚠️ MISSING - Define exact demo scripts:

```markdown
#### Scenario 1: Task Management (⚠️ MISSING minutes)
1. Judge: "Hey Panda"
2. Robot: [Response: ⚠️ MISSING]
3. Judge: "Set an alarm for 3 PM"
4. Robot: [Response: ⚠️ MISSING]
5. Judge: "What's the temperature?"
6. Robot: [Response: ⚠️ MISSING]
[⚠️ MISSING - Complete this scenario]

#### Scenario 2: Autonomous Navigation (⚠️ MISSING minutes)
[⚠️ MISSING - Define complete scenario]

#### Scenario 3: Safety Features (⚠️ MISSING minutes)
[⚠️ MISSING - Define complete scenario]

#### Scenario 4: AI Integration (⚠️ MISSING minutes)
[⚠️ MISSING - Define complete scenario]
```

---

## 26. Deployment & Maintenance

### Installation Procedure

⚠️ MISSING - Provide step-by-step setup:

```bash
# ⚠️ MISSING - Complete installation script

# 1. System update
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install system dependencies
sudo apt-get install -y \
    ⚠️ MISSING  # python3-dev?
    ⚠️ MISSING  # portaudio19-dev?
    ⚠️ MISSING  # Other dependencies?

# 3. Install Python packages
pip3 install -r requirements.txt

# 4. Configure system
⚠️ MISSING  # Enable I2C?
⚠️ MISSING  # Enable SPI for ADC?
⚠️ MISSING  # Set GPIO permissions?

# 5. Upload Arduino code
⚠️ MISSING  # How to upload motor_controller.ino?

# 6. Configure WiFi
⚠️ MISSING  # How to set WiFi credentials?

# 7. Set up autostart
⚠️ MISSING  # systemd service? cron @reboot?
```

### Auto-Start Configuration

⚠️ MISSING - Define startup behavior:

```bash
# Should robot start automatically on boot?
AUTOSTART_ENABLED = ⚠️ MISSING  # True/False

# If yes, provide systemd service file or cron job
# ⚠️ MISSING - Create service file template
```

### Update & Backup Procedures

⚠️ MISSING - Define maintenance procedures:

```bash
# How to backup configuration
⚠️ MISSING

# How to backup SD card
⚠️ MISSING

# How to update code
⚠️ MISSING  # git pull? Manual copy?

# How to rollback if update fails
⚠️ MISSING
```

### Remote Access

⚠️ MISSING - Define remote management:

```bash
# SSH access
SSH_ENABLED = ⚠️ MISSING        # True/False
SSH_PORT = ⚠️ MISSING           # 22 or custom?
SSH_USER = ⚠️ MISSING           # pi? custom user?

# Remote debugging
⚠️ MISSING  # VNC? Other remote desktop?

# Remote logging
⚠️ MISSING  # Send logs to remote server?
```

---

## 27. Documentation Standards

### Code Documentation Requirements

⚠️ MISSING - Define documentation standards:

```python
# Every function should have:
# - Brief description
# - Parameters with types
# - Return value with type
# - Exceptions that can be raised
# - Usage example (for complex functions)

# ⚠️ MISSING - Confirm required documentation level:
# - All functions documented?
# - Only public functions?
# - Include internal logic comments?

# Example docstring format (needs confirmation):
"""
def function_name(param1: int, param2: str) -> bool:
    '''
    Brief one-line description.
    
    Longer description if needed, explaining
    what the function does and why.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 < 0
        IOError: When cannot access hardware
        
    Example:
        >>> result = function_name(5, "test")
        >>> print(result)
        True
    '''
    pass
"""
```

### README Maintenance

⚠️ MISSING - Define README update policy:

```markdown
# When to update README:
- After adding new features?
- After changing hardware?
- After changing pin configurations?
- After competition?

# What to include in README:
⚠️ MISSING - Current README complete or needs additions?
```

---

## 28. Security Considerations

### API Key Security

⚠️ MISSING - Define security practices:

```python
# API keys should NOT be in git repository
# ⚠️ MISSING - How to manage secrets?

# Option 1: Environment variables
# export OPENAI_API_KEY="sk-..."

# Option 2: .env file (gitignored)
# Create .env with keys, load with python-dotenv

# Option 3: Separate config file (gitignored)
# config/secrets.py (not tracked in git)

# Which method to use?
SECRET_MANAGEMENT = "⚠️ MISSING"
```

### Email Security

⚠️ MISSING - Define email security:

```python
# Gmail App Passwords
# ⚠️ MISSING - Document how to generate app password
# ⚠️ MISSING - Where to store securely?

# Email content in emergency
# ⚠️ MISSING - What information to include?
# - GPS coordinates only?
# - Robot status?
# - Recent sensor readings?
# - Camera snapshot?
```

---

## 29. Performance Optimization

### Resource Optimization

⚠️ MISSING - Define optimization strategies:

```python
# CPU Usage Optimization
# - Which operations can be cached?
# - Which imports can be lazy-loaded?
# - Which loops can be optimized?

# Memory Optimization
# - Maximum queue sizes?
# - When to clear caches?
# - When to release resources?

# Startup Time Optimization
# - Parallel initialization?
# - Lazy loading of heavy modules?
# - Skip non-critical checks?

# Response Time Optimization
# - Pre-load common phrases?
# - Cache API responses?
# - Reduce polling frequency?
```

---

## 30. Competition-Specific Information

### Arena Specifications

⚠️ MISSING - Document competition environment:

```python
# Arena Dimensions
ARENA_SIZE = (⚠️ MISSING, ⚠️ MISSING)  # meters (width, height)
ARENA_SURFACE = "⚠️ MISSING"           # tile? wood? carpet?
ARENA_OBSTACLES = "⚠️ MISSING"         # What to expect?

# Demonstration Time Limits
DEMO_TIME_TOTAL = ⚠️ MISSING           # minutes
DEMO_TIME_SETUP = ⚠️ MISSING           # minutes

# Judging Criteria
JUDGING_CRITERIA = [
    "⚠️ MISSING",  # Innovation?
    "⚠️ MISSING",  # Technical complexity?
    "⚠️ MISSING",  # Practical application?
    "⚠️ MISSING"   # Presentation?
]
```

### Backup Plans

⚠️ MISSING - Define contingency plans:

```markdown
#### If motors fail:
⚠️ MISSING - Demonstrate other features without movement?

#### If internet unavailable at venue:
⚠️ MISSING - Switch to offline mode? Use mobile hotspot?

#### If sensor fails during demo:
⚠️ MISSING - Continue without or have spare parts?

#### If power runs out:
⚠️ MISSING - Have backup batteries? Keep robot plugged in?
```

### Presentation Materials

⚠️ MISSING - List required materials:

```markdown
[ ] Poster/Banner: ⚠️ MISSING dimensions
[ ] Slides: ⚠️ MISSING number of slides
[ ] Video demonstration: ⚠️ MISSING duration
[ ] Printed documentation: ⚠️ MISSING pages
[ ] Business cards/Contact info
[ ] ⚠️ MISSING - Other materials?
```

---

## 31. Future Enhancements Roadmap

### Phase 1: Post-Competition Improvements

⚠️ MISSING - Prioritize future features:

```markdown
High Priority:
[ ] ⚠️ MISSING
[ ] ⚠️ MISSING
[ ] ⚠️ MISSING

Medium Priority:
[ ] ⚠️ MISSING
[ ] ⚠️ MISSING

Low Priority:
[ ] ⚠️ MISSING
```

### Phase 2: Advanced Features

⚠️ MISSING - Define long-term vision:

```markdown
# Sign Language Recognition
⚠️ MISSING - Which library/model to use?
⚠️ MISSING - Training dataset?
⚠️ MISSING - Accuracy requirements?

# Morse Code Input
⚠️ MISSING - Via button? Via audio?
⚠️ MISSING - Speed requirements?

# Mobile App
⚠️ MISSING - Flutter? React Native? Native?
⚠️ MISSING - Features required?
```

---

## 32. Glossary & Abbreviations

⚠️ MISSING - Define all technical terms:

```markdown
**STT**: Speech-to-Text
**TTS**: Text-to-Speech
**GPIO**: General Purpose Input/Output
**I²C**: Inter-Integrated Circuit (communication protocol)
**PWM**: Pulse Width Modulation
**ADC**: Analog-to-Digital Converter
⚠️ MISSING - Add more terms used in project
```

---

## 33. Contact & Support

### Team Contact Information

⚠️ MISSING - Provide contact details:

```markdown
**Primary Contact**: ⚠️ MISSING (email)
**Hardware Issues**: ⚠️ MISSING (team member + email)
**Software Issues**: ⚠️ MISSING (team member + email)

**Project Repository**: https://github.com/AmpleVoice/Productivity-Asistant-robot
**Documentation**: ⚠️ MISSING (wiki link?)
**Issue Tracker**: ⚠️ MISSING (GitHub issues?)
```

### Support Resources

⚠️ MISSING - List helpful resources:

```markdown
**Raspberry Pi Documentation**: ⚠️ MISSING
**Arduino Documentation**: ⚠️ MISSING
**Library Documentation**: ⚠️ MISSING
**Community Forums**: ⚠️ MISSING
**Tutorial Videos**: ⚠️ MISSING
```

---

## 🎯 Completion Status

Use this checklist to track which sections are complete:

```markdown
HARDWARE SPECIFICATIONS:
[ ] Section 1: Pin Mappings
[ ] Section 2: Serial Protocol
[ ] Section 8: Power Specs

CONFIGURATION:
[ ] Section 3: API Keys
[ ] Section 4: Sensor Thresholds
[ ] Section 5: Audio Config
[ ] Section 12: Tech Stack Choices

BEHAVIOR DEFINITIONS:
[ ] Section 6: Intent Patterns
[ ] Section 7: Movement Parameters
[ ] Section 10: States & Errors
[ ] Section 11: LCD Formats
[ ] Section 23: Default Behaviors

ARCHITECTURE:
[ ] Section 13: Threading
[ ] Section 14: Timing Requirements
[ ] Section 15: State Machine
[ ] Section 16: Memory Requirements
[ ] Section 17: Network Requirements
[ ] Section 22: Implementation Guidelines

OPERATIONS:
[ ] Section 18: Calibration
[ ] Section 19: Error Recovery
[ ] Section 20: Logging
[ ] Section 26: Deployment

CODE:
[ ] Section 9: Dependencies
[ ] Section 21: Arduino Code
[ ] Section 24: Code Examples

TESTING:
[ ] Section 25: Test Checklist
[ ] Section 30: Competition Info

DOCUMENTATION:
[ ] Section 27: Doc Standards
[ ] Section 28: Security
[ ] Section 29: Optimization
[ ] Section 31: Roadmap
[ ] Section 32: Glossary
[ ] Section 33: Contacts
```

---

## ✅ When This File is Complete

Once all "⚠️ MISSING" markers are filled in, you will have:

1. **Complete hardware specifications** - Any engineer can wire it
2. **Complete software specifications** - Any developer can code it
3. **Complete behavior definitions** - AI knows exactly how it should work
4. **Complete examples** - Ready-to-copy-paste working code
5. **Complete testing procedures** - Can validate everything works

**Result**: Any AI can generate **production-ready, copy-paste code** with <5% clarification questions.

---

## 📝 Notes for AI Code Generation

When an AI reads this completed specification:

1. **Start with** README.md for overview
2. **Then read** PROJECT_SPEC.md for complete technical details
3. **Generate code** module by module, referencing specific sections
4. **Use examples** from Section 24 as templates
5. **Follow guidelines** from Section 22 for consistency
6. **Test against** checklist in Section 25

**The AI should NOT need to ask about**:
- Pin numbers (Section 1)
- Command formats (Section 2)
- Thresholds (Section 4)
- Default behaviors (Section 23)
- Error handling (Section 19, 22)
- Implementation patterns (Section 22)

**The AI MAY still ask about**:
- Specific edge cases not covered
- Optimization preferences
- Code style preferences (if Section 22 unclear)
- Testing strategy details (if Section 25 unclear)

---

**End of PROJECT_SPEC.md**