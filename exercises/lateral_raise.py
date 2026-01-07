import mediapipe as mp
from utils.weighted_angle import weighted_angle
from utils.smoothing import EMAFilter

mp_pose = mp.solutions.pose

class LateralRaise:
    def __init__(self):
        self.counter = 0
        import mediapipe as mp
        from utils.weighted_angle import weighted_angle
        from utils.smoothing import EMAFilter

        mp_pose = mp.solutions.pose

        class LateralRaise:
            def __init__(self):
                self.counter = 0
                self.stage = None
                self.feedback = ""
                self.shoulder_filter = EMAFilter(alpha=0.25)

            def analyze(self, lm):
                hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
                shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

                raw_angle, conf = weighted_angle(hip, shoulder, elbow)
                if conf < 0.6:
                    return {"reps": self.counter, "feedback": "Arm not visible", "angle": None}

                angle = self.shoulder_filter.update(raw_angle)

                if angle < 30:
                    self.stage = "down"

                if angle > 80 and self.stage == "down":
                    self.stage = "up"
                    self.counter += 1
                    self.feedback = "Good raise"

                if angle > 120:
                    self.feedback = "Too high — shoulder strain"

                return {
                    "reps": self.counter,
                    "angle": round(angle, 1),
                    "feedback": self.feedback
                }
