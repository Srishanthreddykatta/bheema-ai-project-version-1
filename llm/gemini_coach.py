import os
import google.generativeai as genai

def get_coaching_feedback(exercise, reps, form_quality):
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return "Set up your Gemini API key to receive feedback."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Provide brief fitness coaching feedback for {exercise} exercise with {reps} reps and {form_quality}% form quality."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Workout complete! {reps} reps of {exercise} with {form_quality:.0f}% form quality."
