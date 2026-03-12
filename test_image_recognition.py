import cv2
import numpy as np

# ✅ Load Trained Model and Labels
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_trained.yml')
label_dict = np.load('labels.npy', allow_pickle=True).item()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ✅ Load Test Image
img = cv2.imread('test.jpg')  # 👉 Change filename if needed
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

for (x, y, w, h) in faces:
    roi_gray = gray[y:y+h, x:x+w]

    id_, conf = recognizer.predict(roi_gray)

    if conf < 70:
        name = label_dict[id_]
        confidence_text = f"{name} ({100 - conf:.2f}%)"
        color = (0, 255, 0)
    else:
        confidence_text = "Unknown"
        color = (0, 0, 255)

    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
    cv2.putText(img, confidence_text, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

cv2.imshow('Test Image Recognition', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
