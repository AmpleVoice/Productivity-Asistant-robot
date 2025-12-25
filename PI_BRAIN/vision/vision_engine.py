import sys
import os
import threading
import time
import cv2
import numpy as np

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from camera.camera_manager import CameraManager
from config import settings

# MediaPipe
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

DEBUG_VIEW = True  # Set False on Raspberry Pi for performance

class VisionEngine(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self._lock = threading.Lock()
        self._stopped = threading.Event()

        self.cam = None
        self.latest_frame = None
        self.target_center = None
        self.latest_faces = []
        self.latest_pose_landmarks = []

        # Face detection
        cascade_path = os.path.join(project_root, "vision", "cascades", "haarcascade_frontalface_default.xml")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        # MediaPipe Pose
        model_path = os.path.join(project_root, 'vision', 'cascades', 'pose_landmarker_full.task')
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=False)
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)


    def run(self):
        self.cam = CameraManager()
        frame_count = 0
        print("[Vision] Vision thread started.")

        while not self._stopped.is_set():
            frame = self.cam.read_frame()
            if frame is None:
                time.sleep(0.05)
                continue

            frame_count += 1
            processed_frame, target_center, faces, pose_landmarks = self.process_frame(frame, frame_count)

            with self._lock:
                self.latest_frame = processed_frame
                self.target_center = target_center
                self.latest_faces = faces
                self.latest_pose_landmarks = pose_landmarks

        self.cam.release()
        print("[Vision] Vision thread stopped.")

    def stop(self):
        self._stopped.set()

    def process_frame(self, frame, frame_count):
        target_center = None
        pose_landmarks = []

        # Resize for performance
        small_frame = cv2.resize(frame, (320, 240))
        
        # Convert the BGR image to RGB.
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # Create a MediaPipe Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)


        # ---- 1. Pose detection ----
        detection_result = self.pose_detector.detect(mp_image)

        if detection_result.pose_landmarks:
            pose_landmarks = detection_result.pose_landmarks
            # Get shoulders midpoint as main target
            landmarks = detection_result.pose_landmarks[0]
            left_shoulder = landmarks[11] # mp.solutions.pose.PoseLandmark.LEFT_SHOULDER
            right_shoulder = landmarks[12] # mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER

            # Convert to pixel coordinates
            h, w, _ = small_frame.shape
            x = int((left_shoulder.x + right_shoulder.x) / 2 * w)
            y = int((left_shoulder.y + right_shoulder.y) / 2 * h)
            target_center = (x, y)

            if DEBUG_VIEW:
                # Draw shoulders and center
                cv2.circle(small_frame, (int(left_shoulder.x * w), int(left_shoulder.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(small_frame, (int(right_shoulder.x * w), int(right_shoulder.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(small_frame, target_center, 5, (255, 0, 0), -1)
                # Draw all landmarks
                for landmark_list in pose_landmarks:
                    for landmark in landmark_list:
                        cv2.circle(small_frame, (int(landmark.x * w), int(landmark.y * h)), 2, (0,0,255), -1)


        # ---- 2. Face detection (fallback / interaction) ----
        faces = []
        if frame_count % 10 == 0 or target_center is None:
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                if DEBUG_VIEW:
                    cv2.rectangle(small_frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            # If pose not detected, set target_center to first face
            if target_center is None and len(faces) > 0:
                x, y, w, h = faces[0]
                target_center = (x + w // 2, y + h // 2)

        # ---- 3. Optional debug window ----
        if DEBUG_VIEW:
            cv2.imshow("VisionEngine", small_frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.stop()

        return small_frame, target_center, faces, pose_landmarks

    # --- Thread-safe getters ---
    def get_latest_frame(self):
        with self._lock:
            return self.latest_frame

    def get_target_position(self):
        with self._lock:
            return self.target_center

    def get_latest_faces(self):
        with self._lock:
            return self.latest_faces

    def get_latest_pose_landmarks(self):
        with self._lock:
            return self.latest_pose_landmarks

    def get_detection_data(self):
        with self._lock:
            return {
                "frame": self.latest_frame,
                "center": self.target_center,
                "faces": self.latest_faces,
                "pose_landmarks": self.latest_pose_landmarks
            }
