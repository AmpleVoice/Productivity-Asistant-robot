import random
from datetime import datetime

# ============================================================
# INTENT KEYWORDS (LOCAL NLU LAYER)
# ============================================================

INTENTS = {
    "greet": [
        "hello", "hi", "hey", "good morning", "good afternoon",
        "good evening", "hey robot", "hello robot"
    ],

    "status": [
        "how are you", "how are you doing", "are you okay",
        "status", "system status", "are you fine"
    ],

    "temperature": [
        "temperature", "how hot", "how cold", "is it hot",
        "is it cold", "weather here", "room temperature"
    ],

    "time": [
        "time", "what time", "current time", "tell me the time"
    ],

    "date": [
        "date", "today's date", "what day is it"
    ],

    "follow": [
        "follow me", "come here", "move with me", "track me"
    ],

    "stop": [
        "stop", "freeze", "halt", "don't move", "stay here"
    ],

    "idle": [
        "idle", "relax", "wait", "do nothing", "stand by"
    ],

    "turn_left": [
        "turn left", "rotate left", "look left"
    ],

    "turn_right": [
        "turn right", "rotate right", "look right"
    ],

    "thanks": [
        "thanks", "thank you", "appreciate it", "nice job"
    ],

    "goodbye": [
        "bye", "goodbye", "see you", "see you later", "farewell"
    ],

    "introduce": [
        "who are you", "introduce yourself", "what are you",
        "tell me about yourself"
    ]
}

# ============================================================
# RESPONSE BANKS
# ============================================================

GREETINGS = [
    "Hello!",
    "Hi there!",
    "Hey! I'm ready.",
    "Greetings!",
    "Hello, how can I help you?",
    "Nice to see you!"
]

STATUS = [
    "I'm doing great.",
    "All systems are working well.",
    "I'm fine and fully operational.",
    "Everything is running smoothly.",
    "Systems are stable and active."
]

TEMP_RESPONSES = [
    "It's about {t} degrees here.",
    "I sense around {t} degrees.",
    "The temperature is approximately {t} degrees.",
    "My sensors report {t} degrees.",
    "Ambient temperature is {t} degrees."
]

TEMP_REACTIONS = {
    "hot": [
        "It's quite warm.",
        "That temperature is on the high side.",
        "My cooling systems are active."
    ],
    "cold": [
        "It's rather cold.",
        "That temperature feels low.",
        "I would recommend warm clothing."
    ],
    "normal": [
        "The temperature is comfortable.",
        "Conditions are ideal.",
        "This is a good temperature for operation."
    ]
}

GOODBYES = [
    "Goodbye!",
    "See you later!",
    "Signing off.",
    "Talk to you soon.",
    "Powering down interaction mode."
]

THANKS = [
    "You're welcome!",
    "Happy to help!",
    "Anytime.",
    "Glad I could assist."
]

INTRODUCTIONS = [
    "I'm Panda Robot, an autonomous assistant designed to help and interact.",
    "I'm a smart robot built to move, sense, and communicate.",
    "I'm your robotic assistant, combining AI and robotics.",
    "I'm a mobile robot capable of interaction and navigation."
]

# ============================================================
# RESPONSE FUNCTIONS
# ============================================================

def greet():
    return random.choice(GREETINGS)

def status():
    return random.choice(STATUS)

def temperature(t):
    if t >= 30:
        mood = random.choice(TEMP_REACTIONS["hot"])
    elif t <= 15:
        mood = random.choice(TEMP_REACTIONS["cold"])
    else:
        mood = random.choice(TEMP_REACTIONS["normal"])

    return f"{random.choice(TEMP_RESPONSES).format(t=t)} {mood}"

def get_time():
    now = datetime.now().strftime("%I:%M %p")
    return random.choice([
        f"It's {now}.",
        f"The current time is {now}.",
        f"My internal clock shows {now}."
    ])

def get_date():
    today = datetime.now().strftime("%B %d, %Y")
    return random.choice([
        f"Today is {today}.",
        f"It's {today}.",
        f"The date today is {today}."
    ])

def say_goodbye():
    return random.choice(GOODBYES)

def thank_you():
    return random.choice(THANKS)

def introduce():
    return random.choice(INTRODUCTIONS)

# ============================================================
# INTENT DETECTION (SIMPLE & FAST)
# ============================================================

def detect_intent(text):
    text = text.lower()

    for intent, keywords in INTENTS.items():
        for word in keywords:
            if word in text:
                return intent

    return "unknown"
