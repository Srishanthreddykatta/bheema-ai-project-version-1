import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import mediapipe as mp
from pose_detector import PoseDetector
from exercises.bicep_curl import BicepCurl
from exercises.lateral_raise import LateralRaise
from exercises.pushup import Pushup
from exercises.squat import Squat
from exercises.lunge import Lunge
from exercises.plank import Plank
from exercises.mountain_climber import MountainClimber
from user_config.user_profile import UserProfile
from memory.session_memory import SessionMemory
from feedback.voice import VoiceCoach
from utils.save_session import save_session
from analysis.fatigue import fatigue_score
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Pose AI - Fitness Tracker")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1a1a1a")
        
        # Initialize modules
        self.pose_detector = PoseDetector()
        self.voice_coach = VoiceCoach()
        self.memory = SessionMemory()
        
        # User data
        self.user = None
        self.selected_exercise = None
        self.exercise_instance = None
        self.is_workout_running = False
        self.cap = None
        
        # Workout tracking
        self.rep_times = []
        self.rom_values = []
        self.last_rep_count = 0
        self.rep_start_time = None
        self.current_rom = 0
        
        # Feedback tracking
        self.last_feedback_time = 0
        self.feedback_cooldown = 2  # seconds
        
        # Show welcome screen
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        """Display welcome screen"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        title = tk.Label(frame, text="🏋️ GYM POSE AI", font=("Arial", 48, "bold"), 
                        fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=30)
        
        subtitle = tk.Label(frame, text="AI-Powered Fitness Tracking", 
                           font=("Arial", 20), fg="#cccccc", bg="#1a1a1a")
        subtitle.pack(pady=10)
        
        desc = tk.Label(frame, text="Track your exercises with real-time form analysis\nand voice coaching", 
                       font=("Arial", 14), fg="#999999", bg="#1a1a1a", justify=tk.CENTER)
        desc.pack(pady=20)
        
        btn_frame = tk.Frame(frame, bg="#1a1a1a")
        btn_frame.pack(pady=50)
        
        btn = tk.Button(btn_frame, text="START WORKOUT", command=self.show_bmi_screen,
                       bg="#00ff00", fg="#000000", font=("Arial", 16, "bold"),
                       padx=30, pady=15, cursor="hand2")
        btn.pack()
    
    def show_bmi_screen(self):
        """Display BMI form screen"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        title = tk.Label(frame, text="PERSONAL INFO", font=("Arial", 32, "bold"), 
                        fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=20)
        
        # Name
        tk.Label(frame, text="Name:", font=("Arial", 14), fg="#cccccc", bg="#1a1a1a").pack(anchor="w", pady=(20, 5))
        name_entry = tk.Entry(frame, font=("Arial", 12), width=40)
        name_entry.pack(fill=tk.X, pady=(0, 20))
        name_entry.insert(0, "User")
        
        # Height
        tk.Label(frame, text="Height (cm):", font=("Arial", 14), fg="#cccccc", bg="#1a1a1a").pack(anchor="w", pady=(20, 5))
        height_entry = tk.Entry(frame, font=("Arial", 12), width=40)
        height_entry.pack(fill=tk.X, pady=(0, 20))
        height_entry.insert(0, "170")
        
        # Weight
        tk.Label(frame, text="Weight (kg):", font=("Arial", 14), fg="#cccccc", bg="#1a1a1a").pack(anchor="w", pady=(20, 5))
        weight_entry = tk.Entry(frame, font=("Arial", 12), width=40)
        weight_entry.pack(fill=tk.X, pady=(0, 20))
        weight_entry.insert(0, "70")
        
        # Age
        tk.Label(frame, text="Age:", font=("Arial", 14), fg="#cccccc", bg="#1a1a1a").pack(anchor="w", pady=(20, 5))
        age_entry = tk.Entry(frame, font=("Arial", 12), width=40)
        age_entry.pack(fill=tk.X, pady=(0, 20))
        age_entry.insert(0, "25")
        
        # Gender
        tk.Label(frame, text="Gender:", font=("Arial", 14), fg="#cccccc", bg="#1a1a1a").pack(anchor="w", pady=(20, 5))
        gender_var = tk.StringVar(value="M")
        gender_frame = tk.Frame(frame, bg="#1a1a1a")
        gender_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="M", 
                      bg="#1a1a1a", fg="#cccccc", selectcolor="#00ff00").pack(anchor="w")
        tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="F", 
                      bg="#1a1a1a", fg="#cccccc", selectcolor="#00ff00").pack(anchor="w")
        
        # Display BMI
        bmi_label = tk.Label(frame, text="", font=("Arial", 14), fg="#ffff00", bg="#1a1a1a")
        bmi_label.pack(pady=20)
        
        def update_bmi(*args):
            try:
                h = float(height_entry.get())
                w = float(weight_entry.get())
                if h > 0 and w > 0:
                    bmi = w / ((h/100) ** 2)
                    bmi_label.config(text=f"BMI: {bmi:.1f}")
            except:
                pass
        
        height_entry.bind("<KeyRelease>", update_bmi)
        weight_entry.bind("<KeyRelease>", update_bmi)
        
        update_bmi()
        
        # Buttons
        btn_frame = tk.Frame(frame, bg="#1a1a1a")
        btn_frame.pack(pady=30)
        
        def proceed():
            try:
                height = float(height_entry.get())
                weight = float(weight_entry.get())
                age = int(age_entry.get())
                name = name_entry.get()
                gender = gender_var.get()
                
                if height <= 0 or weight <= 0 or age <= 0:
                    messagebox.showerror("Error", "Please enter valid positive values")
                    return
                
                self.user = UserProfile(
                    height_cm=height,
                    weight_kg=weight,
                    age=age,
                    gender=gender,
                    name=name
                )
                self.show_exercise_selection()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        tk.Button(btn_frame, text="NEXT", command=proceed,
                 bg="#00ff00", fg="#000000", font=("Arial", 14, "bold"),
                 padx=40, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="BACK", command=self.show_welcome_screen,
                 bg="#666666", fg="#ffffff", font=("Arial", 14, "bold"),
                 padx=40, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
    
    def show_exercise_selection(self):
        """Display exercise selection screen"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        title = tk.Label(frame, text="SELECT EXERCISE", font=("Arial", 32, "bold"), 
                        fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=20)
        
        user_info = tk.Label(frame, 
                            text=f"{self.user.name} | Height: {self.user.height_cm}cm | Weight: {self.user.weight_kg}kg | BMI: {self.user.get_bmi():.1f}",
                            font=("Arial", 12), fg="#cccccc", bg="#1a1a1a")
        user_info.pack(pady=10)
        
        # Exercise buttons
        exercises = [
            ("💪 Bicep Curl", BicepCurl),
            ("🏋️ Pushup", Pushup),
            ("🦵 Squat", Squat),
            ("🏃 Lunge", Lunge),
            ("😤 Plank", Plank),
            ("⛏️ Lateral Raise", LateralRaise),
            ("🏔️ Mountain Climber", MountainClimber),
        ]
        
        button_frame = tk.Frame(frame, bg="#1a1a1a")
        button_frame.pack(pady=30)
        
        for exercise_name, exercise_class in exercises:
            def make_command(name, cls):
                def cmd():
                    self.selected_exercise = name
                    self.exercise_instance = cls()
                    self.show_workout_screen()
                return cmd
            
            tk.Button(button_frame, text=exercise_name, 
                     command=make_command(exercise_name, exercise_class),
                     bg="#0066cc", fg="#ffffff", font=("Arial", 12, "bold"),
                     width=30, pady=10, cursor="hand2").pack(pady=8)
        
        # Back button
        tk.Button(frame, text="BACK", command=self.show_bmi_screen,
                 bg="#666666", fg="#ffffff", font=("Arial", 12, "bold"),
                 padx=40, pady=10, cursor="hand2").pack(pady=20)
    
    def show_workout_screen(self):
        """Display live workout tracking screen"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top bar
        top_bar = tk.Frame(main_frame, bg="#222222")
        top_bar.pack(fill=tk.X, padx=10, pady=10)
        
        exercise_label = tk.Label(top_bar, text=self.selected_exercise, 
                                 font=("Arial", 20, "bold"), fg="#00ff00", bg="#222222")
        exercise_label.pack(side=tk.LEFT, padx=20)
        
        quit_btn = tk.Button(top_bar, text="QUIT", command=self.end_workout,
                            bg="#ff3333", fg="#ffffff", font=("Arial", 12, "bold"),
                            cursor="hand2")
        quit_btn.pack(side=tk.RIGHT, padx=20, pady=5)
        
        # Video and stats container
        content_frame = tk.Frame(main_frame, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video panel
        self.video_label = tk.Label(content_frame, bg="#000000", width=480, height=360)
        self.video_label.pack(side=tk.LEFT, padx=10)
        
        # Stats panel
        stats_frame = tk.Frame(content_frame, bg="#222222")
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        tk.Label(stats_frame, text="WORKOUT STATS", font=("Arial", 16, "bold"),
                fg="#00ff00", bg="#222222").pack(pady=10)
        
        self.rep_label = tk.Label(stats_frame, text="REPS: 0", font=("Arial", 24, "bold"),
                                 fg="#ffff00", bg="#222222")
        self.rep_label.pack(pady=15)
        
        self.angle_label = tk.Label(stats_frame, text="ANGLE: 0°", font=("Arial", 14),
                                   fg="#00ccff", bg="#222222")
        self.angle_label.pack(pady=10)
        
        self.feedback_label = tk.Label(stats_frame, text="FEEDBACK: Ready", 
                                      font=("Arial", 12), fg="#cccccc", bg="#222222",
                                      wraplength=250, justify=tk.CENTER)
        self.feedback_label.pack(pady=15)
        
        self.fatigue_label = tk.Label(stats_frame, text="FATIGUE: 0%", font=("Arial", 14),
                                     fg="#ff6600", bg="#222222")
        self.fatigue_label.pack(pady=10)
        
        self.form_label = tk.Label(stats_frame, text="FORM: 100%", font=("Arial", 14),
                                  fg="#00cc00", bg="#222222")
        self.form_label.pack(pady=10)
        
        self.time_label = tk.Label(stats_frame, text="TIME: 00:00", font=("Arial", 12),
                                  fg="#999999", bg="#222222")
        self.time_label.pack(pady=10)
        
        # Start workout
        self.is_workout_running = True
        self.workout_start_time = time.time()
        self.cap = cv2.VideoCapture(0)
        
        # Voice announcement
        self.voice_coach.announce(f"Starting {self.selected_exercise}")
        
        # Start video feed thread
        self.video_thread = threading.Thread(target=self.update_video_feed, daemon=True)
        self.video_thread.start()
    
    def update_video_feed(self):
        """Update video feed and track exercise"""
        while self.is_workout_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Pose detection
            result = self.pose_detector.process(frame)
            
            if result.pose_landmarks:
                frame = self.pose_detector.draw(frame, result.pose_landmarks)
                
                # Exercise analysis
                output = self.exercise_instance.analyze(result.pose_landmarks.landmark)
                reps = output["reps"]
                angle = output.get("angle")
                feedback = output.get("feedback", "")
                
                # Track ROM
                if angle is not None:
                    self.current_rom = max(self.current_rom, angle)
                
                # Check for rep completion
                if reps > self.last_rep_count:
                    now = time.time()
                    if self.rep_start_time is not None:
                        self.rep_times.append(now - self.rep_start_time)
                        self.rom_values.append(self.current_rom)
                    
                    self.rep_start_time = now
                    self.current_rom = 0
                    self.last_rep_count = reps
                    
                    # Voice announcement for new rep
                    self.voice_coach.announce(f"Perfect! Rep {reps}")
                
                # Calculate fatigue and form
                fatigue = fatigue_score(self.rep_times, self.rom_values)
                form_quality = max(0, 100 - fatigue)
                
                # Update UI labels
                self.update_stats(reps, angle, feedback, fatigue, form_quality)
                
                # Voice feedback for form issues
                current_time = time.time()
                if current_time - self.last_feedback_time > self.feedback_cooldown:
                    if feedback and feedback != "Good raise" and feedback != "Good rep":
                        self.voice_coach.announce(feedback)
                        self.last_feedback_time = current_time
            
            # Add text to frame
            elapsed = int(time.time() - self.workout_start_time)
            cv2.putText(frame, f"REPS: {reps if result.pose_landmarks else 0}", 
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            
            # Convert to PhotoImage
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, dst=frame)
            img = Image.fromarray(frame)
            img = img.resize((480, 360), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)
            self.root.update()
            
            time.sleep(0.03)
    
    def update_stats(self, reps, angle, feedback, fatigue, form_quality):
        """Update statistics labels"""
        self.rep_label.config(text=f"REPS: {reps}")
        
        if angle is not None:
            self.angle_label.config(text=f"ANGLE: {angle:.1f}°")
        
        feedback_text = feedback if feedback else "Keep going"
        self.feedback_label.config(text=f"FEEDBACK:\n{feedback_text}")
        
        self.fatigue_label.config(text=f"FATIGUE: {fatigue:.0f}%")
        self.form_label.config(text=f"FORM: {form_quality:.0f}%")
        
        elapsed = int(time.time() - self.workout_start_time)
        mins, secs = divmod(elapsed, 60)
        self.time_label.config(text=f"TIME: {mins:02d}:{secs:02d}")
    
    def end_workout(self):
        """End workout and show report"""
        self.is_workout_running = False
        if self.cap:
            self.cap.release()
        
        self.show_report_screen()
    
    def show_report_screen(self):
        """Display workout report"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(frame, text="🎉 WORKOUT COMPLETE!", font=("Arial", 32, "bold"), 
                        fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=20)
        
        # Workout details
        exercise_name = self.selected_exercise.split()[-1]
        reps_done = self.exercise_instance.counter
        elapsed = int(time.time() - self.workout_start_time)
        minutes, seconds = divmod(elapsed, 60)
        
        # Calculate calories
        calories_per_rep = self.user.weight_kg * 0.05  # Rough estimate
        total_calories = reps_done * calories_per_rep
        
        # Calculate average metrics
        avg_rom = sum(self.rom_values) / len(self.rom_values) if self.rom_values else 0
        avg_time_per_rep = sum(self.rep_times) / len(self.rep_times) if self.rep_times else 0
        
        # Report content
        report_text = f"""
        Exercise: {self.selected_exercise}
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        📊 PERFORMANCE METRICS
        
        Total Reps: {reps_done}
        Duration: {minutes}m {seconds}s
        Avg Time/Rep: {avg_time_per_rep:.1f}s
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        💪 FORM METRICS
        
        Avg Range of Motion: {avg_rom:.1f}°
        Final Fatigue: {fatigue_score(self.rep_times, self.rom_values):.0f}%
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        🔥 CALORIES BURNED
        
        Estimated: {total_calories:.0f} calories
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        📈 USER INFO
        
        Name: {self.user.name}
        BMI: {self.user.get_bmi():.1f}
        """
        
        report_label = tk.Label(frame, text=report_text.strip(), 
                               font=("Courier", 12), fg="#cccccc", bg="#1a1a1a",
                               justify=tk.LEFT)
        report_label.pack(pady=20)
        
        # Log to memory
        self.memory.log(exercise_name, reps_done, 0, total_calories)
        
        # Save session
        session_data = {
            "user": {
                "name": self.user.name,
                "height_cm": self.user.height_cm,
                "weight_kg": self.user.weight_kg,
                "bmi": self.user.get_bmi()
            },
            "workout": {
                "exercise": self.selected_exercise,
                "reps": reps_done,
                "duration": f"{minutes}m {seconds}s",
                "avg_time_per_rep": avg_time_per_rep,
                "avg_rom": avg_rom,
                "calories": total_calories
            }
        }
        
        filename = save_session(session_data)
        self.voice_coach.announce(f"Workout saved. Great job! You completed {reps_done} reps")
        
        # Buttons
        btn_frame = tk.Frame(frame, bg="#1a1a1a")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="ANOTHER WORKOUT", command=self.show_exercise_selection,
                 bg="#00ff00", fg="#000000", font=("Arial", 12, "bold"),
                 padx=30, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="HOME", command=self.show_welcome_screen,
                 bg="#0066cc", fg="#ffffff", font=("Arial", 12, "bold"),
                 padx=30, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
