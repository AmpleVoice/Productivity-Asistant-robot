import time
from states import RobotState
from movement_controller import MovementController
import obstacle_avoidance
import speech_engine
import actions

class DecisionEngine:
    def __init__(self, sensors):
        self.sensors = sensors
        self.state = RobotState.IDLE
        self.prev_state = RobotState.IDLE
        self.mover = MovementController()

    def update(self):
        # SAFETY OVERRIDES
        if self.sensors.emergency:
            self.state = RobotState.SAFETY_STOP

        if self.sensors.gas_danger:
            self.state = RobotState.ALARM

        # OBSTACLE CHECK (INTERRUPTS)
        avoided = obstacle_avoidance.avoid(
            self.sensors.front_left,
            self.sensors.front_right
        )

        if avoided:
            return  # resume previous state automatically

        # STATE LOGIC
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

    def handle_voice(self, text):
        t = text.lower()

        if "hello" in t:
            actions.talk(speech_engine.greet())
            self.state = RobotState.INTERACT

        elif "how are you" in t:
            actions.talk(speech_engine.status())

        elif "temperature" in t:
            actions.talk(speech_engine.temperature(self.sensors.temperature))

        elif "follow" in t:
            self.state = RobotState.MOVE

        elif "stop" in t:
            self.state = RobotState.IDLE