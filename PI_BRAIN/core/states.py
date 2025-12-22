from enum import Enum

class RobotState(Enum):
    IDLE = 0
    MOVE = 1          # following
    AVOID_OBSTACLE = 2
    INTERACT = 3
    ALARM = 4
    SAFETY_STOP = 5
