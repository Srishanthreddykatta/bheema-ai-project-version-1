import mediapipe as mp
from utils.weighted_angle import weighted_angle
from utils.smoothing import EMAFilter

mp_pose = mp.solutions.pose

class Lunge:
    def __init__(self):
        self.counter = 0
        import mediapipe as mp
        from utils.weighted_angle import weighted_angle
        from utils.smoothing import EMAFilter

        mp_pose = mp.solutions.pose

        class Lunge:
            def __init__(self):
                self.counter = 0
                self.stage = None
                self.feedback = ""
                self.knee_filter = EMAFilter(alpha=0.3)

            def analyze(self, lm):
                hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
                knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                ankle = lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

                raw_angle, conf = weighted_angle(hip, knee, ankle)
                if conf < 0.6:
                    return {"reps": self.counter, "feedback": "Leg not visible", "angle": None}

                angle = self.knee_filter.update(raw_angle)

                if angle > 160:
                    self.stage = "up"

                if angle < 100 and self.stage == "up":
                    self.stage = "down"
                    self.counter += 1
                    self.feedback = "Nice lunge"

                if angle < 70:
                    self.feedback = "Too deep — protect knee"

                return {
                    "reps": self.counter,
                    "angle": round(angle, 1),
                    "feedback": self.feedback
                }
