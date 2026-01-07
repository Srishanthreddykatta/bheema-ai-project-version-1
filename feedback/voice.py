import pyttsx3

class VoiceCoach:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
    
    def announce(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
