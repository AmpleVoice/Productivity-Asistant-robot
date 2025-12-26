from enum import Enum

class RobotState(Enum):
    IDLE = 0
    MOVE = 1          # following
    SEARCH = 2        # searching for target
    AVOID_OBSTACLE = 3
    INTERACT = 4
    ALARM = 5
    SAFETY_STOP = 6
