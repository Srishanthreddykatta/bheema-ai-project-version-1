import cv2
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API key
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

from pose_detector import PoseDetector
from exercises.lateral_raise import LateralRaise
from user_config.user_profile import UserProfile
from memory.session_memory import SessionMemory
from llm.gemini_coach import get_coaching_feedback
from feedback.voice import VoiceCoach
from utils.save_session import save_session
from analysis.fatigue import fatigue_score

# -----------------------
# USER SETUP (TEMP)
# -----------------------
user = UserProfile(
    height_cm=172,
    weight_kg=70,
    age=22,
    gender="male"
)

memory = SessionMemory()
voice = VoiceCoach()

# -----------------------
# WORKOUT SETUP
# -----------------------
pose = PoseDetector()
exercise = LateralRaise()
cap = cv2.VideoCapture(0)

# -----------------------
# FATIGUE TRACKING STATE
# -----------------------
rep_times = []
rom_values = []
last_rep_count = 0
rep_start_time = None
current_rom = 0

print("Starting workout. Press 'q' to quit...")

# -----------------------
# MAIN LOOP
# -----------------------
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result = pose.process(frame)

        if result.pose_landmarks:
            frame = pose.draw(frame, result.pose_landmarks)

            output = exercise.analyze(result.pose_landmarks.landmark)
            reps = output["reps"]
            angle = output.get("angle")

            # -----------------------
            # TRACK RANGE OF MOTION
            # -----------------------
            if angle is not None:
                current_rom = max(current_rom, angle)

            # -----------------------
            # REP COMPLETION
            # -----------------------
            if reps > last_rep_count:
                now = time.time()

                if rep_start_time is not None:
                    rep_times.append(now - rep_start_time)
                    rom_values.append(current_rom)

                rep_start_time = now
                current_rom = 0
                last_rep_count = reps
                
                # Announce rep
                voice.announce(f"Rep {reps}")

            # -----------------------
            # FATIGUE + FORM SCORES
            # -----------------------
            fatigue = fatigue_score(rep_times, rom_values)
            form_quality = max(0.0, 100 - fatigue)

            # -----------------------
            # UI OVERLAYS
            # -----------------------
            cv2.putText(frame, f"REPS: {reps}",
                        (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (0, 255, 0), 3)
            
            if angle is not None:
                cv2.putText(frame, f"ANGLE: {angle:.1f}°",
                            (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (255, 100, 0), 2)
            
            cv2.putText(frame, f"FATIGUE: {fatigue:.1f}%",
                        (30, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255), 2)
            
            cv2.putText(frame, f"FORM: {form_quality:.1f}%",
                        (30, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2)

        cv2.imshow("Gym Pose AI", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()

# -----------------------
# END OF WORKOUT
# -----------------------
print(f"\nWorkout Complete! Total Reps: {exercise.counter}")

exercise_name = "Lateral Raise"
used_weight = 7.5  # kg
reps_done = exercise.counter

# Simple calorie proxy
calories = reps_done * used_weight * 0.06 if reps_done > 0 else 0

memory.log(exercise_name, reps_done, used_weight, calories)
summary = memory.summary()

print(f"\nSession Summary: {summary}")

# -----------------------
# LLM COACH (POST SESSION)
# -----------------------
try:
    feedback = get_coaching_feedback(exercise_name, reps_done, form_quality)
    print("\n===== WORKOUT FEEDBACK =====\n")
    print(feedback)
except Exception as e:
    print(f"Could not generate Gemini feedback: {e}")

# 💾 SAVE
filename = save_session(summary)
print(f"\nSession saved to {filename}")
