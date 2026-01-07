#!/usr/bin/env python3
"""
Setup script for bheema-ai project
Installs all required dependencies for Gemini API integration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Execute a command and display status"""
    print(f"\n📦 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode == 0:
        print(f"✓ {description} completed successfully")
        return True
    else:
        print(f"✗ {description} failed with error code {result.returncode}")
        return False

def main():
    print("=" * 60)
    print("bheema-ai Setup Script")
    print("=" * 60)
    
    venv_path = Path(".venv310/Scripts/python.exe")
    
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please create it with: py -3.10 -m venv .venv310")
        sys.exit(1)
    
    python_cmd = str(venv_path)
    
    # Check .env file
    if not Path(".env").exists():
        print("\n⚠️ .env file not found!")
        print("Please create a .env file with: GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    print("✓ .env file found")
    
    # Install requirements
    success = run_command(
        f'{python_cmd} -m pip install --upgrade pip',
        "Upgrading pip"
    )
    
    if success:
        success = run_command(
            f'{python_cmd} -m pip install -r requirements.txt',
            "Installing dependencies from requirements.txt"
        )
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run the project with:")
        print(f"  {python_cmd} main.py")
    else:
        print("\n" + "=" * 60)
        print("❌ Setup failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
