import mediapipe as mp
from utils.weighted_angle import weighted_angle
from utils.smoothing import EMAFilter

mp_pose = mp.solutions.pose

class PushUp:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.elbow_filter = EMAFilter(alpha=0.25)
        self.body_filter = EMAFilter(alpha=0.2)

    def analyze(self, lm):
        shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE.value]

        raw_elbow, conf1 = weighted_angle(shoulder, elbow, wrist)
        raw_body, conf2 = weighted_angle(shoulder, hip, knee)

        if min(conf1, conf2) < 0.6:
            return {"reps": self.counter, "feedback": "Body not clear", "angle": None}

        elbow_angle = self.elbow_filter.update(raw_elbow)
        body_angle = self.body_filter.update(raw_body)

        if elbow_angle > 160:
            import mediapipe as mp
            from utils.weighted_angle import weighted_angle
            from utils.smoothing import EMAFilter

            mp_pose = mp.solutions.pose

            class PushUp:
                def __init__(self):
                    self.counter = 0
                    self.stage = None
                    self.feedback = ""
                    self.elbow_filter = EMAFilter(alpha=0.25)
                    self.body_filter = EMAFilter(alpha=0.2)

                def analyze(self, lm):
                    shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                    elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
                    wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                    hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
                    knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE.value]

                    raw_elbow, conf1 = weighted_angle(shoulder, elbow, wrist)
                    raw_body, conf2 = weighted_angle(shoulder, hip, knee)

                    if min(conf1, conf2) < 0.6:
                        return {"reps": self.counter, "feedback": "Body not clear", "angle": None}

                    elbow_angle = self.elbow_filter.update(raw_elbow)
                    body_angle = self.body_filter.update(raw_body)

                    if elbow_angle > 160:
                        self.stage = "up"

                    if elbow_angle < 90 and self.stage == "up":
                        self.stage = "down"
                        self.counter += 1
                        self.feedback = "Good push-up"

                    if body_angle < 160:
                        self.feedback = "Keep back straight"

                    return {
                        "reps": self.counter,
                        "angle": round(elbow_angle, 1),
                        "feedback": self.feedback
                    }
