import sys
import os

# ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.smoothing import EMAFilter


class BicepCurlSim:
    """A small local simulator of the BicepCurl logic that accepts raw angles."""
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.elbow_filter = EMAFilter(alpha=0.25)

    def analyze_raw(self, raw_angle, confidence=0.95):
        if confidence < 0.6:
            return {"reps": self.counter, "feedback": "Arm not visible clearly", "angle": None}

        smooth_angle = self.elbow_filter.update(raw_angle)

        if smooth_angle > 160:
            self.stage = "down"

        if smooth_angle < 40 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.feedback = "Good rep"

        if smooth_angle < 25:
            self.feedback = "Do not over-curl"

        if smooth_angle > 170:
            self.feedback = "Fully extend at bottom"

        return {"reps": self.counter, "angle": round(smooth_angle, 1), "feedback": self.feedback}


def main():
    sim = BicepCurlSim()

    # Simulate frames: extended -> curled -> extended -> curled (two reps)
    sequence = [170]*5 + [130]*3 + [90]*3 + [35]*4 + [170]*5 + [30]*4

    print("Frame	Raw	Smoothed	Reps	Feedback")
    for i, raw in enumerate(sequence, 1):
        out = sim.analyze_raw(raw)
        # compute smoothed value (internal) by reusing returned angle
        print(f"{i}\t{raw}\t{out['angle']}\t{out['reps']}\t{out['feedback']}")


if __name__ == '__main__':
    main()
