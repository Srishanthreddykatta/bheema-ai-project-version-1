# 🏋️ GYM POSE AI - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Windows 10/11
- Webcam
- Python 3.10 installed
- 500MB free disk space

### Step 1: Clone the Repository
```bash
git clone https://github.com/Srishanthreddykatta/bheema-ai-project-version-1.git
cd bheema-ai-project-version-1
```

### Step 2: Create Virtual Environment
```bash
py -3.10 -m venv .venv310
.venv310\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key
Create `.env` file in project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get free API key: https://aistudio.google.com/app/apikey

### Step 5: Run the Application
```bash
python fitness_ui.py
```

## 🎯 Using the App

### Screen 1: Welcome
- Click **START WORKOUT**

### Screen 2: Personal Info
- Enter your details:
  - **Name**: Your name
  - **Height**: In centimeters (e.g., 170)
  - **Weight**: In kilograms (e.g., 70)
  - **Age**: Your age
  - **Gender**: Male/Female
- View calculated **BMI**
- Click **NEXT**

### Screen 3: Exercise Selection
- Choose one of 7 exercises:
  - 💪 Bicep Curl
  - 🏋️ Pushup
  - 🦵 Squat
  - 🏃 Lunge
  - 😤 Plank
  - ⛏️ Lateral Raise
  - 🏔️ Mountain Climber

### Screen 4: Workout
**Left side:** Live video feed with pose skeleton
**Right side:** Real-time stats

**What you see:**
- 🔢 **REPS**: Current rep count
- 📐 **ANGLE**: Joint angle in degrees
- 💬 **FEEDBACK**: Form corrections
- 🔥 **FATIGUE**: Energy level (0-100%)
- ✅ **FORM**: Quality score (0-100%)
- ⏱️ **TIME**: Elapsed workout time

**Voice:**
- "Perfect! Rep 1" when you complete a rep
- "Keep back straight" for form corrections

**To quit:**
- Click **QUIT** button (red)

### Screen 5: Report
See your workout summary:
- Total reps completed
- Workout duration
- Average ROM (Range of Motion)
- Calories burned 🔥
- Your metrics

**Options:**
- **ANOTHER WORKOUT**: Try different exercise
- **HOME**: Go back to start

## 💡 Tips for Best Results

### 📍 Positioning
- Stand 1.5-2 meters from webcam
- Full body visible in frame
- Good lighting (face a light source)
- Clear background

### 👕 What to Wear
- Contrasting colors (light top/dark background)
- Fitted clothing (loose clothes confuse AI)
- Avoid reflective materials

### 🎤 Voice Feedback
- Keep speakers on
- Ensure volume is not muted
- Quiet room for better audio

### 📊 Form Matters
- Do exercises slowly and controlled
- Full range of motion
- Listen to voice feedback
- Adjust form as suggested

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Webcam not found | Check Windows Settings → Privacy → Camera |
| Voice not working | Check system volume, ensure speakers connected |
| No pose detection | Better lighting, full body in frame, stand farther |
| Python version error | Use `py -3.10` only, not `python 3.11` |
| API key error | Verify `.env` file exists, API key is valid |
| GUI not showing | Try minimizing/maximizing window |

## 📱 Features Explained

### Real-time Form Analysis
- AI analyzes your movements in real-time
- Based on 33 body landmarks
- Calculates joint angles
- Provides instant feedback

### Voice Coaching
- Text-to-speech feedback
- Corrects form issues
- Announces perfect reps
- Motivates during workout

### Calorie Calculation
- Based on body weight + exercise + reps
- Formula: Reps × (Weight_kg × 0.05)
- Example: 15 reps × (70kg × 0.05) = 52.5 calories

### Progress Tracking
- All workouts saved as JSON
- Track improvement over time
- Monitor your metrics

## 🎯 Exercise Guide

### 💪 Bicep Curl
- Stand upright, feet shoulder-width apart
- Arms at sides, palms forward
- Curl arms upward, keep elbows stationary
- Lower back to start position

### 🏋️ Pushup
- Standard pushup position
- Lower body until chest near floor
- Push back up to start
- Keep body straight

### 🦵 Squat
- Feet shoulder-width apart
- Lower body by bending knees
- Keep chest up, back straight
- Return to standing

### 🏃 Lunge
- Step forward with one leg
- Lower body until back knee near floor
- Both knees at 90 degrees
- Return and alternate legs

### 😤 Plank
- Forearm plank position
- Keep body straight
- Engage core
- Hold position

### ⛏️ Lateral Raise
- Arms at sides, weights in hands
- Raise arms to shoulder height
- Keep slight elbow bend
- Lower with control

### 🏔️ Mountain Climber
- Plank position
- Alternate bringing knees to chest
- Keep hips level
- Maintain steady pace

## 📊 Understanding Your Results

### Reps
- Number of complete exercise repetitions
- Detected automatically by AI

### Duration
- Total workout time
- Includes setup time

### Avg ROM (Range of Motion)
- 120° = Full range
- 90° = Good form
- 60° = Partial range

### Fatigue
- 0% = Fresh
- 50% = Moderate
- 100% = Exhausted

### Form Quality
- 100% = Perfect form maintained
- 75% = Good, minor form loss
- 50% = Form degrading

### Calories
- Estimated energy expended
- Depends on body weight + exercise + reps

## 🆘 Getting Help

### Common Issues

**"No module named 'mediapipe'"**
```bash
pip install mediapipe==0.10.14
```

**"Cannot find API key"**
- Create `.env` file in project root
- Add: `GEMINI_API_KEY=your_key`

**"Webcam permission denied"**
- Windows Settings → Privacy → Camera
- Allow Python to access camera

**"Python version not compatible"**
```bash
# Use exactly Python 3.10
py -3.10 --version  # Should show 3.10.x
```

## 📞 Support

For issues, visit: https://github.com/Srishanthreddykatta/bheema-ai-project-version-1/issues

## 🎉 Ready to Start?

```bash
python fitness_ui.py
```

**Let's get fit with AI! 💪🤖**

---

Last updated: January 2026
