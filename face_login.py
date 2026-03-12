# face_login.py — Astra's Face Recognition Module with Live Video Name Overlay

import cv2
import numpy as np
from datetime import datetime
import pygetwindow as gw
import pyautogui
import time

def move_window_to_top_right(window_title):
    time.sleep(1.5)
    try:
        for w in gw.getWindowsWithTitle(window_title):
            if w.title:
                screen_width, screen_height = pyautogui.size()
                new_x = screen_width - w.width
                new_y = 0
                w.moveTo(new_x, new_y)
                break
    except Exception as e:
        print(f"⚠️ Could not move window: {e}")

def face_login():
    print("🔒 Starting face verification...")

    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('face_trained.yml')
        label_dict = np.load('labels.npy', allow_pickle=True).item()
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        return False

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    verified = False
    success_count = 0

    log_file = open("access_log.txt", "a", encoding="utf-8")

    window_title = "🔒 Astra Face Login - Press Q to quit"
    move_called = False

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # 🔁 Mirror the image horizontally

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roi_gray)
            name = "Unknown"
            color = (0, 0, 255)

            if conf < 60:
                name = label_dict.get(id_, "Unknown")
                if name != "Unknown":
                    success_count += 1
                    if success_count >= 5:
                        verified = True
                log_file.write(f"{datetime.now()} - ✅ ACCESS: {name} - {100 - conf:.2f}%\n")
                color = (0, 255, 0)
            else:
                log_file.write(f"{datetime.now()} - ❌ DENIED: Unknown - {100 - conf:.2f}%\n")

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{name} ({100 - conf:.2f}%)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow(window_title, frame)

        if not move_called:
            move_window_to_top_right(window_title)
            move_called = True

        key = cv2.waitKey(1)
        if key == ord('q') or verified:
            break

    cap.release()
    cv2.destroyAllWindows()
    log_file.close()

    if verified:
        print("✅ Face verified successfully.")
        return True
    else:
        print("❌ Face verification failed.")
        return False

if __name__ == "__main__":
    face_login()
