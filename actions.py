import os
import pyautogui
import webbrowser
import subprocess
from jokes import jokes
import random
from ask_llama import ask_llama
from datetime import datetime
from word2number import w2n
import time
# Initialize TTS engine
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"🔊 Astra: {text}")
    engine.say(text)
    engine.runAndWait()

pyautogui.FAILSAFE = True


def open_app_safely(path, name):
    try:
        if path.startswith("http"):
            webbrowser.open(path)
        elif ".lnk" in path.lower():
            subprocess.Popen(['explorer', path])
        elif path.endswith(".exe") or path.startswith("explorer.exe"):
            subprocess.Popen(path)
        else:
            os.startfile(path)
        return True
    except Exception as e:
        speak(f"Sorry, couldn't open {name}.")
        print(f"❌ Error opening {name}:", e)
        return False


APP_MAP = {

    # 🎵 Media (✅ FIXED Spotify to real AppID)
    "spotify": r"C:\Users\LENOVO\Desktop\Spotify - Shortcut.lnk",

    # 📱 Communication (✅ FIXED WhatsApp to real AppID)
    "what's up": r"C:\Users\LENOVO\Desktop\WhatsApp Beta - Shortcut",
    "zoom": os.path.expanduser("~\\Desktop\\Zoom.lnk"),

    # 🗂️ Folders
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),

    # 🧲 System Utilities
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "paint": "mspaint.exe",

    # 🌐 Browsers
    # ✅ FIXED Brave path to use .lnk shortcut
    "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "edge": r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "brave": os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Brave.lnk"),

    # 💼 Productivity
    "vs code": r"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "visual studio code": r"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "notepad++": r"C:\\Program Files\\Notepad++\\notepad++.exe",
    "obsidian": "obsidian",
    "onenote": "Microsoft.Office.ONENOTE.EXE.15",

    # 🏬 UWP Apps via shortcut (unchanged if they work)
    "app store": os.path.expanduser("~\\Desktop\\App Store.lnk"),
    "calendar": os.path.expanduser("~\\Desktop\\Calendar.lnk"),
    "lenovo vantage": os.path.expanduser("~\\Desktop\\Lenovo Vantage.lnk"),
    "weather": os.path.expanduser("~\\Desktop\\Weather.lnk"),

    # 📺 Online
    "youtube": "https://www.youtube.com",
}

def get_time():
    return datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.now().strftime("%A, %d %B %Y")

def get_weather():
    return "It looks sunny today in Delhi!"  # Placeholder

def handle_command(text, speak):
    text = text.lower()

    # Universal Open
    for name, path in APP_MAP.items():
        if f"open {name}" in text or text.strip().endswith(name):
            speak(f"Opening {name}")
            open_app_safely(path, name)
            return True

    # Universal Close
    if "close" in text:
        # 🔴 Close current tab
        if "close window" in text:
            pyautogui.hotkey("alt", "f4")
            speak("Closed the tab.")
            return True

        # ❌ Close an app from APP_MAP
        for name, path in APP_MAP.items():
            if name in text:
                exe_name = os.path.basename(path).replace('"', '')
                speak(f"Closing {name}")
                os.system(f"taskkill /f /im {exe_name}")
                return True

        speak("Sorry, I couldn't find which app to close.")
        return True

    # 🌐 Web actions
    if "open google" in text:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return True


    # 🔽 Minimize window
    elif "minimize" in text or "minimise" in text:
        pyautogui.hotkey("win", "m")
        time.sleep(0.2)
        pyautogui.press("n")
        speak("Window minimized.")
        return True

    # ⬆️ Maximize window
    elif "maximize" in text or "maximise" in text:
        pyautogui.hotkey("win", "up")
        time.sleep(0.2)
        pyautogui.press("x")
        speak("Window maximized.")
        return True

    elif "joke" in text:
        speak(random.choice(jokes))
        return True
    elif "time" in text:
        speak(f"The time is {get_time()}.")
        return True
    elif "date" in text:
        speak(f"Today is {get_date()}.")
        return True
    elif "weather" in text:
        speak(get_weather())
        return True
    elif "search for" in text:
        query = text.split("search for")[-1].strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return True

    # 📸 Screenshot
    elif "take screenshot" in text or "screenshot" in text:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"screenshot_{int(time.time())}.png"
        filepath = os.path.join(desktop_path, filename)
        pyautogui.screenshot(filepath)
        speak(f"Screenshot saved on your Desktop as {filename}")
        return True


    # ⌨️ Typing
    elif "type" in text:
        to_type = text.split("type")[-1].strip()
        pyautogui.write(to_type)
        speak("Typed the message.")
        return True

    # 🔽 Scroll / Mouse
    elif "scroll down" in text:
        pyautogui.scroll(-1000)
        speak("Scrolling down")
        return True
    elif "scroll up" in text:
        pyautogui.scroll(1000)
        speak("Scrolling up")
        return True
    elif "move mouse" in text:
        pyautogui.moveTo(100, 100, duration=1)
        speak("Mouse moved.")
        return True

    # 📋 Paste
    elif "paste" in text:
        pyautogui.hotkey("ctrl", "v")
        speak("Pasted.")
        return True

    # 💚 Click
    elif "click" in text:
        pyautogui.click()
        speak("Mouse clicked.")
        return True

    # 🔊 Volume
    elif "mute" in text:
        pyautogui.press("volumemute")
        speak("Volume muted.")
        return True
    elif "volume up" in text:
        pyautogui.press("volumeup")
        speak("Increasing volume.")
        return True
    elif "volume down" in text:
        pyautogui.press("volumedown")
        speak("Decreasing volume.")
        return True

    # 🔒 Lock
    elif "lock screen" in text:
        speak("Locking your screen.")
        subprocess.run("rundll32.exe user32.dll,LockWorkStation")
        return True
    elif "shut down" in text or "power off" in text:
        speak("Shutting down the computer.")
        os.system("shutdown /s /t 5")
        return True

    # 🤖 Basic replies
    elif text in ["hello", "hi", "hey"]:
        speak("Hello! How can I assist you today?")
        return True
    elif "how are you" in text:
        speak("I'm functioning perfectly. How can I help you?")
        return True
    elif "who are you" in text or "what are you" in text:
        speak("I'm Astra, your personal voice and gesture-powered assistant.")
        return True
    elif "thank you" in text or "thanks" in text:
        speak("You're welcome!")
        return True
    elif "who made you" in text:
        speak("I was created by Abishek, built with Python, Vosk, LLaMA, and love.")
        return True
    elif "repeat after me" in text:
        phrase = text.split("repeat after me")[-1].strip()
        speak(phrase if phrase else "What should I repeat?")
        return True
    elif "goodbye" in text or "bye" in text:
        speak("Goodbye! Have a great day!")
        return True
    elif "your name" in text:
        speak("My name is Astra.")
        return True
    elif "are you real" in text:
        speak("I'm as real as code and silicon can be!")
        return True

    # 🧲 Voice-based Math
    elif any(op in text for op in ["plus", "minus", "into", "divided by", "multiply", "add", "subtract", "x"]):
        speak("Let me calculate that for you...")
        try:
            expression = text.lower()
            expression = expression.replace("plus", "+").replace("add", "+")
            expression = expression.replace("minus", "-").replace("subtract", "-")
            expression = expression.replace("into", "*").replace("multiply", "*").replace("x", "*")
            expression = expression.replace("divided by", "/").replace("divide", "/")

            parts = []
            buffer = ""

            for word in expression.split():
                if word in "+-*/":
                    if buffer:
                        num = w2n.word_to_num(buffer.strip())
                        parts.append(str(num))
                        buffer = ""
                    parts.append(word)
                else:
                    buffer += word + " "

            if buffer:
                num = w2n.word_to_num(buffer.strip())
                parts.append(str(num))

            eval_expr = " ".join(parts)
            result = eval(eval_expr)

            speak(f"The result is {result}")
            subprocess.Popen(["calc.exe"])
            time.sleep(1)
            pyautogui.write(str(result), interval=0.1)
            return True

        except Exception as e:
            speak("Sorry, I couldn't process the math.")
            print("🔚 Error:", e)
            return True

    return False

def handle_unknown(command, speak):
    speak("Let me ask ChatGPT for you.")
    shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "ChatGPT - Shortcut.lnk")
    try:
        subprocess.Popen(['explorer', shortcut_path])
        time.sleep(5)
        pyautogui.write(command, interval=0.05)
        pyautogui.press("enter")
    except Exception as e:
        speak("Sorry, I couldn’t open ChatGPT.")
        print("🔚 Error opening ChatGPT:", e)
