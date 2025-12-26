import json
import os

CONFIG_PATH = "config/scheduler.json"

# Create the file if it doesn't exist
if not os.path.exists("config"):
    os.makedirs("config")

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"alarms": {}}, f, indent=4)

def load_data():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def add_alarm(alarm_id, time_str):
    data = load_data()
    data["alarms"][alarm_id] = {
        "time": time_str,   # format "HH:MM"
        "enabled": True
    }
    save_data(data)
    print(f"✅ Alarm '{alarm_id}' added at {time_str}")

def delete_alarm(alarm_id):
    data = load_data()
    if alarm_id in data["alarms"]:
        del data["alarms"][alarm_id]
        save_data(data)
        print(f"🗑️ Alarm '{alarm_id}' deleted")
    else:
        print(f"❌ Alarm '{alarm_id}' not found")

def modify_alarm(alarm_id, time=None, enabled=None):
    data = load_data()
    if alarm_id in data["alarms"]:
        if time is not None:
            data["alarms"][alarm_id]["time"] = time
        if enabled is not None:
            data["alarms"][alarm_id]["enabled"] = enabled
        save_data(data)
        print(f"✏️ Alarm '{alarm_id}' modified")
    else:
        print(f"❌ Alarm '{alarm_id}' not found")
