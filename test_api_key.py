#!/usr/bin/env python3
"""Quick test to verify Gemini API key is configured"""

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if api_key and api_key.startswith('AIza'):
    print(f"✓ GEMINI_API_KEY configured: {api_key[:20]}...")
else:
    print("✗ GEMINI_API_KEY not configured properly")
    exit(1)

# Try importing the library
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    print("✓ Google Generative AI library loaded and configured")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

print("\n✓ All checks passed! API key is ready to use.")
