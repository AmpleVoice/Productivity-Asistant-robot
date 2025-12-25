import cv2
import time
from vision.vision_engine import VisionEngine

def main():
    """
    Main function to run the vision system test.
    """
    print("--- Vision System Test ---")
    print("This will test the threaded VisionEngine.")
    print("A window will open showing the camera feed.")
    print("The system will detect and circle red objects.")
    print("Press 'q' in the window to exit.")

    # 1. Initialize and start the Vision Engine
    vision_engine = VisionEngine()
    vision_engine.start()

    # 2. Main loop to display results
    try:
        while True:
            # Get the latest detection data from the engine
            detection_data = vision_engine.get_detection_data()
            
            frame = detection_data["frame"]
            if frame is not None:
                # The frame is already processed by the engine with bounding boxes
                cv2.imshow("Camera", frame)

            # Get target position and print it
            target_pos = detection_data["center"]
            if target_pos:
                print(f"Target (torso center) detected at: {target_pos}")

            # Get and print face detections
            faces = detection_data["faces"]
            if len(faces) > 0:
                print(f"Faces detected: {faces}")
            
            # Get and print pose landmark detections
            pose_landmarks = detection_data["pose_landmarks"]
            if pose_landmarks:
                print(f"Pose landmarks detected.")

            # Check for exit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(0.05) # Small delay to prevent busy-waiting

    finally:
        # 3. Cleanly stop the vision engine and close windows
        print("\n--- Exiting vision test ---")
        vision_engine.stop()
        vision_engine.join() # Wait for the thread to finish
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

