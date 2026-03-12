import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
labels = []
label_dict = {}
label_count = 0

dataset_path = 'dataset'

for person_name in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person_name)
    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(label_count)
    label_dict[label_count] = person_name
    label_count += 1

recognizer.train(faces, np.array(labels))
recognizer.save('face_trained.yml')
np.save('labels.npy', label_dict)

print("✅ Model trained and saved as face_trained.yml and labels.npy")
