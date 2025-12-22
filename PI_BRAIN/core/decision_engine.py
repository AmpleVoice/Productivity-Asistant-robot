from core.states import RobotState
from core.movement_controller import MovementController
from core import obstacle_avoidance
from core import speech_engine
from core import actions

class DecisionEngine:
    def __init__(self, sensors):
        self.sensors = sensors
        self.state = RobotState.IDLE
        self.prev_state = RobotState.IDLE
        self.mover = MovementController()
        print("[DecisionEngine] Initialized")

    def update(self):
        sensor_data = self.sensors.read() if self.sensors else {}

        # Safety
        gas = sensor_data.get("gas", {}).get("mq9", {})
        if gas.get("dangerous_CO", False):
            if self.state != RobotState.ALARM:
                print("[DecisionEngine] ⚠ ALARM: Dangerous CO!")
            self.state = RobotState.ALARM

        ultrasonic = sensor_data.get("ultrasonic", {}).get("ultrasonic", {})
        left = ultrasonic.get("left")
        right = ultrasonic.get("right")
        if left is not None and right is not None:
            if obstacle_avoidance.avoid(left, right):
                return

        # Execute state
        if self.state == RobotState.SAFETY_STOP:
            self.mover.send("S")
        elif self.state == RobotState.ALARM:
            actions.ring_alarm()
            self.mover.send("S")
        elif self.state == RobotState.MOVE:
            self.mover.send("F")
        elif self.state == RobotState.INTERACT:
            pass
        elif self.state == RobotState.IDLE:
            self.mover.send("S")

    def handle_voice(self, text: str):
        print(f"[DecisionEngine] Processing voice: '{text}'")
        result = speech_engine.process(text, self.sensors)
        if not result:
            return
        response = result.get("response")
        if response:
            print(f"[DecisionEngine] Response: {response}")
            actions.talk(response)
        new_state = result.get("state")
        if new_state is not None and new_state != self.state:
            self.prev_state = self.state
            self.state = new_state
            print(f"[DecisionEngine] State: {self.prev_state} → {self.state}")
