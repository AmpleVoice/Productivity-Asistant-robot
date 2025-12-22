import random
from datetime import datetime
from core.states import RobotState

# ---------------- INTENTS ----------------
INTENTS = {
    "greet": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
    "status": ["how are you", "are you okay", "status", "system status"],
    "temperature": ["temperature", "how hot", "how cold", "is it hot", "is it cold"],
    "time": ["time", "what time", "current time"],
    "date": ["date", "today's date", "what day"],
    "follow": ["follow me", "come here", "move with me", "track me"],
    "stop": ["stop", "freeze", "halt", "don't move", "stay here"],
    "idle": ["idle", "relax", "wait", "do nothing", "stand by"],
    "turn_left": ["turn left", "rotate left", "look left"],
    "turn_right": ["turn right", "rotate right", "look right"],
    "thanks": ["thanks", "thank you", "appreciate it"],
    "goodbye": ["bye", "goodbye", "see you later", "farewell"],
    "introduce": ["who are you", "introduce yourself", "what are you"]
}

# ---------------- RESPONSES ----------------
RESPONSES = {
    "greet": ["Hello!", "Hi there!", "Hey! I'm ready.", "Greetings!", "Nice to see you!"],
    "status": ["I'm doing great.", "All systems operational.", "Everything is running smoothly."],
    "temp_base": ["It's about {t} degrees.", "I sense around {t} degrees.", "Temperature is {t} degrees."],
    "temp_hot": ["It's quite warm.", "That's on the high side."],
    "temp_cold": ["It's rather cold.", "That feels low.", "Recommend warm clothing."],
    "temp_normal": ["Temperature is comfortable.", "Conditions are ideal."],
    "time": ["It's {time}.", "Current time is {time}.", "My clock shows {time}."],
    "date": ["Today is {date}.", "It's {date}.", "The date is {date}."],
    "follow": ["Okay, I'll follow you.", "Following you now.", "Lead the way!"],
    "stop": ["Stopping now.", "I've stopped.", "Halted."],
    "idle": ["Going idle.", "I'll wait here.", "Standing by."],
    "turn_left": ["Turning left.", "Rotating left."],
    "turn_right": ["Turning right.", "Rotating right."],
    "thanks": ["You're welcome!", "Happy to help!", "Anytime."],
    "goodbye": ["Goodbye!", "See you later!", "Talk to you soon."],
    "introduce": ["I'm Panda Robot, your autonomous assistant.", "I'm a smart robot built to help."]
}

# ---------------- INTENT DETECTION ----------------
def detect_intent(text: str) -> str:
    text = text.lower()
    for intent, keywords in INTENTS.items():
        if any(word in text for word in keywords):
            return intent
    return "unknown"

# ---------------- PROCESS FUNCTION ----------------
def process(text: str, sensors):
    intent = detect_intent(text)
    result = {"intent": intent, "response": None, "state": None}

    if intent == "greet":
        result["response"] = random.choice(RESPONSES["greet"])
        result["state"] = RobotState.INTERACT

    elif intent == "status":
        result["response"] = random.choice(RESPONSES["status"])

    elif intent == "temperature":
        temp = None
        if sensors:
            data = sensors.read()
            temp = data.get("temperature")

        if temp is not None:
            base = random.choice(RESPONSES["temp_base"]).format(t=temp)
            if temp >= 30:
                mood = random.choice(RESPONSES["temp_hot"])
            elif temp <= 15:
                mood = random.choice(RESPONSES["temp_cold"])
            else:
                mood = random.choice(RESPONSES["temp_normal"])
            result["response"] = f"{base} {mood}"
        else:
            result["response"] = "I cannot read the temperature right now."

    elif intent == "time":
        now = datetime.now().strftime("%I:%M %p")
        result["response"] = random.choice(RESPONSES["time"]).format(time=now)

    elif intent == "date":
        today = datetime.now().strftime("%B %d, %Y")
        result["response"] = random.choice(RESPONSES["date"]).format(date=today)

    elif intent == "follow":
        result["response"] = random.choice(RESPONSES["follow"])
        result["state"] = RobotState.MOVE

    elif intent == "stop":
        result["response"] = random.choice(RESPONSES["stop"])
        result["state"] = RobotState.IDLE

    elif intent == "idle":
        result["response"] = random.choice(RESPONSES["idle"])
        result["state"] = RobotState.IDLE

    elif intent == "turn_left":
        result["response"] = random.choice(RESPONSES["turn_left"])
        result["state"] = RobotState.MOVE

    elif intent == "turn_right":
        result["response"] = random.choice(RESPONSES["turn_right"])
        result["state"] = RobotState.MOVE

    elif intent == "thanks":
        result["response"] = random.choice(RESPONSES["thanks"])

    elif intent == "goodbye":
        result["response"] = random.choice(RESPONSES["goodbye"])
        result["state"] = RobotState.IDLE

    elif intent == "introduce":
        result["response"] = random.choice(RESPONSES["introduce"])

    else:
        result["response"] = "Sorry, I didn't understand that."

    return result
