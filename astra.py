# astra.py — Voice-Controlled Desktop Automation Assistant (with GUI, LLaMA, NLP, Gestures, Face Login)

import pyttsx3
import pyautogui
import subprocess
import os
import time
from datetime import datetime

from voice import listen
from actions import handle_command, handle_unknown
from log import log_command
from gui import AstraGUI
from ask_llama import ask_llama  # 🧠 Offline LLM here
from face_login import face_login  # 🔒 Face verification module
from gesture import GestureDetector  # ✋ Class-based gesture detector

# Initialize TTS engine
engine = pyttsx3.init()
gui = None

def speak(text):
    print(f"🔊 Astra: {text}")
    try:
        gui.add_log(f"🔊 Astra: {text}")
    except:
        pass  # GUI not available or already destroyed
    engine.say(text)
    engine.runAndWait()

def main():
    global gui
    gui = AstraGUI()
    gui.add_log("🧠 Astra online. Awaiting secure access...")
    speak("Astra online. Awaiting secure access...")

    # ✅ Step 1: Face Login
    if face_login():
        speak("Access granted. You may now use gestures to give commands.")
        gui.add_log("✅ Face verified. Gesture listening enabled.")

        gesture = GestureDetector()  # Start webcam once and reuse

        while True:
            gui.add_log("✋ Waiting for palm gesture to listen...")
            gui.add_log("Show your palm to speak.")

            gesture_name = None
            while not gesture_name:
                gesture_name = gesture.detect_palm_once()
                if gesture_name == "exit":
                    speak("Gesture detection exited.")
                    gui.add_log("🚪 Gesture window closed by user.")
                    gesture.close_camera()
                    gui.add_log("🛑 Astra session ended.")
                    gui.start()
                    return

            # 🧠 Handle special gestures (peace / thumbs up)
            if gesture.handle_gesture_action(gesture_name, speak):
                continue  # Skip voice input if gesture was handled directly

            # 🎙️ Only allow voice input if palm is shown
            if gesture_name != "palm":
                continue

            # 🗣️ Now accept voice
            text = listen()
            if not text:
                continue

            speak(f"You said: {text}")
            log_command(text)

            if text.lower() in ["exit", "shutdown astra"]:
                speak("Shutting down. Goodbye!")
                break

            handled = handle_command(text, speak)
            if not handled:
                handle_unknown(text, speak)

        gesture.close_camera()

    else:
        speak("Access denied. Closing Astra.")
        gui.add_log("❌ Face verification failed.")

    gui.add_log("🛑 Astra session ended.")
    gui.start()

if __name__ == "__main__":
    main()
