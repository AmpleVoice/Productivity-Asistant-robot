import threading
import os
import cv2

# Try to import MediaPipe Tasks API; if unavailable, fall back to OpenCV Haar cascades
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    _HAS_MEDIAPIPE = True
except Exception:
    mp = None
    python = None
    vision = None
    _HAS_MEDIAPIPE = False

from camera.camera_manager import CameraManager, project_root

class VisionEngine(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._lock = threading.Lock()
        self._stopped = threading.Event()
        self._ready_event = threading.Event()

        self.cam = None
        self.target_center = None
        self.target_width = None  # pixel width between shoulders

        # Initialize pose detector (prefer MediaPipe Tasks; otherwise fall back to Haar face cascade)
        self._use_mediapipe = False
        self.face_cascade = None

        if _HAS_MEDIAPIPE and python and vision:
            try:
                model_path = os.path.join(project_root, 'vision', 'cascades', 'pose_landmarker_full.task')
                base_options = python.BaseOptions(model_asset_path=model_path)
                options = vision.PoseLandmarkerOptions(base_options=base_options)
                self.pose_detector = vision.PoseLandmarker.create_from_options(options)
                self._use_mediapipe = True
            except Exception as e:
                print(f"[Vision] MediaPipe model init failed: {e} - falling back to Haar cascade")
                self.pose_detector = None

        if not self._use_mediapipe:
            # Use Haar cascade face detector as a lightweight fallback
            cascade_path = os.path.join(project_root, 'vision', 'cascades', 'haarcascade_frontalface_default.xml')
            if os.path.exists(cascade_path):
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
            else:
                print("[Vision] No Haar cascade found; face detection disabled")

    def run(self):
        try:
            self.cam = CameraManager()
            # Indicate that the vision thread has successfully started and camera is available
            self._ready_event.set()
            print("[Vision] Started")
        except Exception as e:
            print(f"[Vision] Failed to start camera: {e}")
            # Mark ready so waiters don't hang; thread will stop
            self._ready_event.set()
            return

        while not self._stopped.is_set():
            frame = self.cam.read_frame()
            if frame is None:
                continue

            center, width = self.process_frame(frame)

            with self._lock:
                self.target_center = center
                self.target_width = width

        self.cam.release()

    def stop(self):
        self._stopped.set()

    def wait_ready(self, timeout=None):
        """Wait until the vision thread indicates readiness. Returns True if ready, False on timeout."""
        return self._ready_event.wait(timeout)

    def process_frame(self, frame):
        small = cv2.resize(frame, (320, 240))

        if self._use_mediapipe and self.pose_detector and mp:
            rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            result = self.pose_detector.detect(mp_image)

            if not result.pose_landmarks:
                return None, None

            landmarks = result.pose_landmarks[0]
            # Fallback if landmarks don't have shoulder indices
            try:
                left = landmarks[11]
                right = landmarks[12]
                h, w, _ = small.shape
                x_center = int((left.x + right.x) / 2 * w)
                y_center = int((left.y + right.y) / 2 * h)
                shoulder_width = abs(left.x - right.x) * w
                return (x_center, y_center), shoulder_width
            except Exception:
                return None, None

        # Haar cascade fallback: detect faces and approximate shoulder width
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        if self.face_cascade is None:
            return None, None

        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) == 0:
            return None, None

        # Choose the largest face as the target
        x, y, fw, fh = max(faces, key=lambda r: r[2] * r[3])
        center = (int(x + fw / 2), int(y + fh / 2))
        # Approximate shoulder width as 1.3x face width
        shoulder_width = fw * 1.3
        return center, shoulder_width

    def get_target(self):
        with self._lock:
            return {
                "center": self.target_center,
                "width": self.target_width
            }
