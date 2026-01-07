import mediapipe as mp
from utils.weighted_angle import weighted_angle
from utils.smoothing import EMAFilter

mp_pose = mp.solutions.pose

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.knee_filter = EMAFilter(alpha=0.3)
        self.hip_filter = EMAFilter(alpha=0.25)

    def analyze(self, lm):
        hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        ankle = lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        raw_knee, conf1 = weighted_angle(hip, knee, ankle)
        raw_hip, conf2 = weighted_angle(shoulder, hip, knee)

        if min(conf1, conf2) < 0.6:
            return {"reps": self.counter, "feedback": "Lower body not visible", "angle": None}

        knee_angle = self.knee_filter.update(raw_knee)
        hip_angle = self.hip_filter.update(raw_hip)

        if knee_angle > 160:
            self.stage = "up"

        if knee_angle < 100 and self.stage == "up":
            self.stage = "down"
            self.counter += 1
            self.feedback = "Good squat"

        if knee_angle > 150:
            self.feedback = "Go deeper"

        if hip_angle < 160:
            self.feedback = "Chest falling forward"

        return {
            "reps": self.counter,
            "angle": round(knee_angle, 1),
            "feedback": self.feedback
        }
