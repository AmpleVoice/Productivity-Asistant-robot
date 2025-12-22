import time
from core import actions

OBSTACLE_DISTANCE = 25  # cm

def avoid(front_left, front_right):
    """
    Returns True if avoidance happened
    """

    if front_left < OBSTACLE_DISTANCE and front_right < OBSTACLE_DISTANCE:
        actions.stop()
        time.sleep(0.2)
        actions.move_backward()
        time.sleep(0.4)
        actions.turn_left()
        time.sleep(0.4)
        return True

    if front_right < OBSTACLE_DISTANCE:
        actions.turn_left()
        time.sleep(0.25)
        actions.move_forward()
        time.sleep(0.3)
        actions.turn_right()
        time.sleep(0.25)
        return True

    if front_left < OBSTACLE_DISTANCE:
        actions.turn_right()
        time.sleep(0.25)
        actions.move_forward()
        time.sleep(0.3)
        actions.turn_left()
        time.sleep(0.25)
        return True

    return False
