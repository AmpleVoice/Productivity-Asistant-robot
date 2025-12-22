# config/settings.py

# --- Ultrasonic ---
ULTRASONIC_INTERVAL = 0.1
SAFE_DISTANCE_CM = 30

# --- Gas ---
MQ9_INTERVAL = 5
GAS_THRESHOLD = 300

# --- Scheduler ---
SCHEDULER_INTERVAL = 60  # every minute

# --- LCD ---
LCD_INTERVAL = 0.5

# --- States ---
STATE_IDLE = "IDLE"
STATE_MOVING = "MOVING"
STATE_ALARM = "ALARM"
STATE_ERROR = "ERROR"
