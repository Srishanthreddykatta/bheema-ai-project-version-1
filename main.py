import cv2
import mediapipe as mp
import pyttsx3
from pose_detector import PoseDetector
from exercises.bicep_curl import BicepCurl

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# MediaPipe drawing utilities for skeleton visualization
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def main():
    cap = cv2.VideoCapture(0)
    pose = PoseDetector()
    exercise = BicepCurl()
    prev_reps = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result = pose.process(frame)

        # Draw skeleton (landmarks and connections)
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

            output = exercise.analyze(result.pose_landmarks.landmark)

            # Voice announcement when new rep is completed
            if output["reps"] > prev_reps:
                rep_message = f"Good rep! {output['reps']} reps completed"
                print(rep_message)
                engine.say(rep_message)
                engine.runAndWait()
                prev_reps = output["reps"]

            if output["angle"] is not None:
                cv2.putText(frame, f"Angle: {output['angle']}",
                            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            cv2.putText(frame, f"Reps: {output['reps']}",
                        (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

            cv2.putText(frame, output["feedback"],
                        (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        # Display press 'c' to close hint
        cv2.putText(frame, "Press 'c' to close",
                    (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow("Gym Pose AI", frame)

        # Check for 'c' key to close webcam
        key = cv2.waitKey(10) & 0xFF
        if key == ord("c"):
            print("Closing webcam...")
            break

    cap.release()
    cv2.destroyAllWindows()
    engine.stop()

if __name__ == "__main__":
    main()
