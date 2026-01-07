from datetime import datetime

class SessionMemory:
    def __init__(self):
        self.history = []

    def log(self, exercise, reps, weight, calories):
        self.history.append({
            "time": datetime.now().isoformat(),
            "exercise": exercise,
            "reps": reps,
            "weight": weight,
            "calories": calories
        })

    def summary(self):
        total_cal = sum(x["calories"] for x in self.history)
        return {
            "total_exercises": len(self.history),
            "total_calories": round(total_cal, 2),
            "details": self.history
        }
