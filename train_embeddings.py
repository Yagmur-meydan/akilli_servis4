import cv2
import mediapipe as mp
import os
import numpy as np
import pickle

mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

data_dir = "students_fixed"
embeddings = []
names = []

# MediaPipe FaceMesh modelini başlat
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def get_embedding(image):
    h, w, _ = image.shape
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return None

    keypoints = []
    for lm in results.multi_face_landmarks[0].landmark:
        keypoints.append([lm.x * w, lm.y * h, lm.z])

    return np.array(keypoints).flatten()

for file in os.listdir(data_dir):
    if not file.lower().endswith(('.jpg','.png','.jpeg')):
        continue
    path = os.path.join(data_dir, file)
    img = cv2.imread(path)
    if img is None:
        continue
    emb = get_embedding(img)
    if emb is not None:
        name = ''.join([c for c in os.path.splitext(file)[0] if c.isalpha()])
        embeddings.append(emb)
        names.append(name)
        print(f"{file} için embedding çıkarıldı.")
    else:
        print(f" {file}: yüz bulunamadı.")

# Kaydet
with open("embeddings.pkl", "wb") as f:
    pickle.dump({"embeddings": embeddings, "names": names}, f)

print("Embedding veritabanı oluşturuldu.")
