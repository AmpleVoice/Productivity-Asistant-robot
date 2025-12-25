import sys
import os

# Add the project root to the Python path to resolve import issues
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import cv2
from config import settings

class CameraManager:
    def __init__(self, source=None):
        """
        Initializes the camera using the source provided or the default from settings.
        :param source: Optional; overrides the default camera source from settings.
        """
        if source is None:
            source = settings.CAMERA_SOURCE
        
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera source {source}")

    def read_frame(self):
        """
        Reads a frame from the camera and resizes it based on settings.
        :return: The resized frame, or None if the frame could not be read.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Resize for faster processing based on centralized settings
        frame = cv2.resize(frame, (settings.FRAME_WIDTH, settings.FRAME_HEIGHT))
        return frame

    def release(self):
        self.cap.release()
