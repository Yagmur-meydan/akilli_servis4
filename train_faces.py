import cv2
import os
import numpy as np
import mediapipe as mp
import pickle

mp_face = mp.solutions.face_detection

data_dir = "students_fixed"
faces = []
labels = []
label_map = {}
inv_map = {}
current_label = 0

with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as detector:
    for file in sorted(os.listdir(data_dir)):
        if not file.lower().endswith(('.jpg','.png','.jpeg')):
            continue
        name = os.path.splitext(file)[0]
        base = ''.join(filter(str.isalpha, name))  # yagmur1 -> yagmur

        if base not in label_map:
            label_map[base] = current_label
            inv_map[current_label] = base
            current_label += 1

        img = cv2.imread(os.path.join(data_dir, file))
        if img is None:
            print("Okunamadı:", file)
            continue
        h, w = img.shape[:2]
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = detector.process(rgb)
        if results.detections:
            det = results.detections[0].location_data.relative_bounding_box
            x1 = max(0, int(det.xmin * w))
            y1 = max(0, int(det.ymin * h))
            x2 = min(w, int((det.xmin + det.width) * w))
            y2 = min(h, int((det.ymin + det.height) * h))
            face = img[y1:y2, x1:x2]
            if face.size == 0:
                continue
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (160, 160))
            faces.append(gray)
            labels.append(label_map[base])
            print("Eklendi:", file, "->", base)
        else:
            print("Yüz bulunamadı:", file)

if len(faces) == 0:
    print("Hiç yüz bulunamadı! Fotoğrafları kontrol et.")
    exit()

faces_np = np.array(faces)
labels_np = np.array(labels)

model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=16, grid_x=8, grid_y=8, threshold=123.0)
model.train(faces_np, labels_np)

model.write("lbph_model.yml")
with open("label_map.pkl", "wb") as f:
    pickle.dump(inv_map, f)

print("Eğitim tamamlandı. Model ve label map oluşturuldu.")
print("Label map:", inv_map)
