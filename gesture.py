import cv2
import mediapipe as mp
import subprocess
import time
import pyautogui
import pygetwindow as gw
import win32gui
import win32con

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

    def move_window_to_top_right(self, title):
        time.sleep(1.5)
        try:
            for w in gw.getWindowsWithTitle(title):
                if w.title:
                    screen_width, screen_height = pyautogui.size()
                    new_x = screen_width - w.width
                    new_y = 0
                    w.moveTo(new_x, new_y)
                    break
        except Exception as e:
            print(f"⚠️ Could not move window: {e}")

    def make_window_always_on_top(self, window_title):
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except Exception as e:
            print(f"⚠️ Could not set always on top: {e}")

    def detect_palm_once(self):
        start_time = time.time()
        gesture_buffer = []
        moved = False
        window_title = "Gesture Detection"
        stable_gesture = None

        while time.time() - start_time < 3:
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            gesture_detected = None

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    lm = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]

                    thumb = lm[tips[0]].x < lm[tips[0] - 1].x
                    index = lm[8].y < lm[6].y
                    middle = lm[12].y < lm[10].y
                    ring = lm[16].y < lm[14].y
                    pinky = lm[20].y < lm[18].y

                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    if all([thumb, index, middle, ring, pinky]):
                        gesture_detected = "palm"
                    elif thumb and not index:
                        gesture_detected = "thumbs_up"
                    elif not thumb and index and middle and not ring and not pinky:
                        gesture_detected = "peace"
                    elif thumb and index and not middle and not ring and not pinky:
                        gesture_detected = "ok"
                    elif not any([thumb, index, middle, ring, pinky]):
                        gesture_detected = "fist"
                    elif index and not any([middle, ring, pinky, thumb]):
                        gesture_detected = "one_finger"
                    elif index and pinky and not middle and not ring:
                        gesture_detected = "rock_sign"
                    elif index and middle and ring and pinky and not thumb:
                        gesture_detected = "spock"
                    elif result.multi_handedness[0].classification[0].label == "Left":
                        gesture_detected = "back_hand"

            gesture_buffer.append(gesture_detected)
            if len(gesture_buffer) > 20:
                gesture_buffer.pop(0)

            if gesture_buffer:
                stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)

            label = stable_gesture if stable_gesture else "Show your palm to speak"
            cv2.putText(frame, label, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if stable_gesture else (0, 0, 255), 2)

            cv2.imshow(window_title, frame)
            self.make_window_always_on_top(window_title)

            if not moved:
                self.move_window_to_top_right(window_title)
                moved = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                return "exit"

        return stable_gesture

    def handle_gesture_action(self, gesture, speak):
        if gesture == "peace":
            speak("Opening Visual Studio Code")
            subprocess.Popen(r"C:\\Users\\LENOVO\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
            return True
        elif gesture == "thumbs_up":
            speak("Opening Lenovo Vantage")
            subprocess.Popen(["explorer.exe", "shell:AppsFolder\\E046963F.LenovoCompanion_k1h2ywk1493x8!App"])
            return True
        elif gesture == "one_finger":
            speak("Opening Obsidian")
            try:
                shortcut_path = r"C:\Users\LENOVO\Desktop\Obsidian - Shortcut.lnk"
                subprocess.Popen(['explorer', shortcut_path])
            except Exception as e:
                speak("Couldn't open Obsidian.")
                print(f"❌ Obsidian launch error:", e)
            return True
        elif gesture == "rock_sign":
            speak("Opening Spotify")
            try:
                shortcut_path = r"C:\Users\LENOVO\Desktop\Spotify - Shortcut.lnk"
                subprocess.Popen(['explorer', shortcut_path])
            except Exception as e:
                speak("Couldn't open Spotify.")
                print(f"❌ Spotify launch error:", e)
            return True
        elif gesture == "ok":
            speak("Locking your screen.")
            subprocess.run("rundll32.exe user32.dll,LockWorkStation")
            return True

        return False

    def close_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
