class UserProfile:
    def __init__(self, height_cm=170, weight_kg=70, age=25, gender='M', name='User'):
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.age = age
        self.gender = gender
        self.name = name
    
    def get_bmi(self):
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)
    
    def __repr__(self):
        return f"UserProfile({self.name}, Age: {self.age}, Height: {self.height_cm}cm, Weight: {self.weight_kg}kg)"
