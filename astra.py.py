# astra.py — Voice-Controlled Desktop Automation Assistant (Phase 1)

import pyttsx3
import pyautogui
import subprocess
import os
import time
from datetime import datetime
from voice import listen
from actions import handle_command
from log import log_command

# Initialize TTS engine
engine = pyttsx3.init()
def speak(text):
    print(f"🔊 Astra: {text}")
    engine.say(text)
    engine.runAndWait()

def main():
    speak("Astra online. Awaiting your command.")
    while True:
        text = listen()
        if not text:
            continue
        speak(f"You said: {text}")
        log_command(text)
        handled = handle_command(text, speak)
        if text.lower() in ["exit", "shutdown astra"]:
            speak("Shutting down. Goodbye!")
            break
        if not handled:
            speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
