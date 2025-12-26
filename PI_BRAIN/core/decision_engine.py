import time

from core.states import RobotState
from core import obstacle_avoidance
from core import speech_engine
from core import actions


class DecisionEngine:
    """
    Main decision-making system for the robot.
    Handles state management, sensor processing, and behavior execution.
    """
    
    # Constants
    VISION_LOST_TIMEOUT = 2.0    # seconds before switching to SEARCH
    TARGET_DISTANCE_PX = 60      # desired shoulder width for following
    FRAME_CENTER_X = 160         # camera frame center X
    FRAME_CENTER_Y = 120         # camera frame center Y

    def __init__(self, sensors, vision=None):
        """
        Initialize the decision engine.
        
        Args:
            sensors: Sensor interface for reading robot sensors
            vision: Vision system for person tracking (required for MOVE state)
        """
        self.sensors = sensors
        self.vision = vision

        self.state = RobotState.IDLE
        self.prev_state = RobotState.IDLE

        self.last_vision_time = None
        self.camera_angle = 90

        # Motor state tracking to avoid repeated stop commands
        self._motors_stopped = True

        print("[DecisionEngine] Initialized")

    # =========================
    # MAIN UPDATE LOOP
    # =========================
    def update(self):
        """Main control loop - called repeatedly to update robot behavior."""
        sensor_data = self.sensors.read() if self.sensors else {}

        # -------------------------
        # 1. GAS SAFETY (HIGHEST PRIORITY)
        # -------------------------
        gas = sensor_data.get("gas", {}).get("mq9", {})
        if gas.get("dangerous_CO", False):
            if self.state != RobotState.ALARM:
                print("[DecisionEngine] ⚠ ALARM: Dangerous CO detected!")
            self.state = RobotState.ALARM

        # -------------------------
        # 2. ALARM STATE HANDLING
        # -------------------------
        if self.state == RobotState.ALARM:
            actions.ring_alarm()
            actions.stop_motors()
            return

        # -------------------------
        # 3. OBSTACLE AVOIDANCE
        # -------------------------
        ultrasonic = sensor_data.get("ultrasonic", {}).get("ultrasonic", {})
        left = ultrasonic.get("left")
        right = ultrasonic.get("right")

        if left is not None and right is not None:
            if obstacle_avoidance.should_avoid(left, right):
                obstacle_avoidance.execute()
                return

        # -------------------------
        # 4. STATE EXECUTION
        # -------------------------
        if self.state == RobotState.SAFETY_STOP:
            self._ensure_stopped()
            
        elif self.state == RobotState.MOVE:
            self._handle_move()
            
        elif self.state == RobotState.SEARCH:
            self._handle_search()
            
        elif self.state == RobotState.INTERACT:
            self._ensure_stopped()
            
        elif self.state == RobotState.IDLE:
            self._ensure_stopped()

    # =========================
    # MOVE STATE (FOLLOW PERSON)
    # =========================
    def _handle_move(self):
        """
        Handle person-following behavior using vision.
        Requires vision system to be available - no blind movement.
        """
        if not self.vision:
            print("[DecisionEngine] WARNING: MOVE state requires vision system")
            actions.stop_motors()
            return

        target = self.vision.get_target()
        center = target.get("center")
        width = target.get("width")
        now = time.time()

        # Vision detected - follow the person
        if center and width:
            self.last_vision_time = now
            self._follow_person(center, width)
            return

        # Vision lost - check timeout
        if self.last_vision_time and (now - self.last_vision_time) > self.VISION_LOST_TIMEOUT:
            print("[DecisionEngine] Vision lost → SEARCH")
            self.prev_state = self.state
            self.state = RobotState.SEARCH
            self._ensure_stopped()

    # =========================
    # SEARCH STATE
    # =========================
    def _handle_search(self):
        """
        Handle search behavior when person is lost.
        Stops and waits for vision to reacquire target.
        """
        self._ensure_stopped()

        if not self.vision:
            return

        target = self.vision.get_target()
        if target.get("center"):
            print("[DecisionEngine] Target found → MOVE")
            self.prev_state = self.state
            self.state = RobotState.MOVE
            self.last_vision_time = time.time()

    # =========================
    # FOLLOW CONTROL
    # =========================
    def _follow_person(self, center, width):
        """
        Execute person-following control using proportional control.
        
        Args:
            center: (x, y) tuple of person's center in frame
            width: shoulder width in pixels
        """
        x, y = center

        # --- Horizontal rotation control ---
        x_error = x - self.FRAME_CENTER_X
        turn = int(x_error * 0.4)

        # --- Distance control ---
        distance_error = self.TARGET_DISTANCE_PX - width
        forward = int(distance_error * 1.2)

        # Clamp values to safe ranges
        forward = max(min(forward, 120), -120)
        turn = max(min(turn, 80), -80)

        # Differential drive
        left_speed = forward - turn
        right_speed = forward + turn

        # Stop if at target distance
        if abs(distance_error) < 8:
            self._ensure_stopped()
        else:
            # When commanding motors, mark them as running
            actions.set_motor_speeds(left_speed, right_speed)
            self._motors_stopped = False

        # --- Vertical camera tracking ---
        y_error = self.FRAME_CENTER_Y - y
        self.camera_angle += int(y_error * 0.05)
        self.camera_angle = max(60, min(120, self.camera_angle))
        actions.set_camera_angle(self.camera_angle)

    # =========================
    # VOICE COMMAND HANDLING
    # =========================
    def handle_voice(self, text: str):
        """
        Process voice commands and update robot state accordingly.
        ALARM state is locked and cannot be changed by voice.
        
        Args:
            text: Transcribed voice command text
        """
        # ALARM state is locked - no voice commands accepted
        if self.state == RobotState.ALARM:
            print("[DecisionEngine] ALARM state locked - voice commands disabled")
            return
            
        print(f"[DecisionEngine] Processing voice: '{text}'")

        result = speech_engine.process(text, self.sensors)
        if not result:
            return

        # Speak response if available
        response = result.get("response")
        if response:
            print(f"[DecisionEngine] Response: {response}")
            actions.talk(response)

        # Update state if command requires it
        new_state = result.get("state")
        if new_state is not None and new_state != self.state:
            self.prev_state = self.state
            self.state = new_state
            print(f"[DecisionEngine] State: {self.prev_state} → {self.state}")

    # =========================
    # INTERNAL HELPERS
    # =========================
    def _ensure_stopped(self):
        """Stop motors only when they were previously running (avoid repeated calls)."""
        if not self._motors_stopped:
            actions.stop_motors()
            self._motors_stopped = True