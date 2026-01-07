import mediapipe as mp
from utils.weighted_angle import weighted_angle
from utils.smoothing import EMAFilter

import mediapipe as mp
from utils.weighted_angle import weighted_angle
from utils.smoothing import EMAFilter

mp_pose = mp.solutions.pose

class BicepCurl:
    def __init__(self):
        # Rep tracking
        self.counter = 0
        self.stage = None
        self.feedback = ""

        # EMA FILTER
        self.elbow_filter = EMAFilter(alpha=0.25)

    def analyze(self, landmarks):
        # Get landmarks
        shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow    = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist    = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # 1) ANGLE + CONFIDENCE
        raw_angle, confidence = weighted_angle(shoulder, elbow, wrist)

        if confidence < 0.6:
            return {
                "reps": self.counter,
                "feedback": "Arm not visible clearly",
                "angle": None
            }

        # 2) TEMPORAL SMOOTHING
        smooth_angle = self.elbow_filter.update(raw_angle)

        # 3) REP LOGIC (ONLY SMOOTHED)
        if smooth_angle > 160:
            self.stage = "down"

        if smooth_angle < 40 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.feedback = "Good rep"

        # 4) FORM FEEDBACK
        if smooth_angle < 25:
            self.feedback = "Do not over-curl"

        if smooth_angle > 170:
            self.feedback = "Fully extend at bottom"

        return {
            "reps": self.counter,
            "angle": round(smooth_angle, 1),
            "feedback": self.feedback
        }

