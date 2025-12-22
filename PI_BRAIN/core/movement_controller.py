import time
import actions

class MovementController:
    def __init__(self):
        self.last_cmd = None
        self.last_time = 0
        self.interval = 0.35

    def send(self, cmd):
        now = time.time()
        if cmd == self.last_cmd and now - self.last_time < self.interval:
            return

        self.last_cmd = cmd
        self.last_time = now

        if cmd == "F":
            actions.move_forward()
        elif cmd == "B":
            actions.move_backward()
        elif cmd == "L":
            actions.turn_left()
        elif cmd == "R":
            actions.turn_right()
        elif cmd == "S":
            actions.stop()
