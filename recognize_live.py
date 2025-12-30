import cv2
import mediapipe as mp
import pickle
import numpy as np
import database
import time
from collections import deque

# Model yükle
model = cv2.face.LBPHFaceRecognizer_create()
model.read("lbph_model.yml")
with open("label_map.pkl", "rb") as f:
    inv_map = pickle.load(f)

mp_face = mp.solutions.face_detection

cap = cv2.VideoCapture(0)
print("Kamera açıldı")

last_seen_name = None
last_seen_time = 0
recent_names = deque(maxlen=10)

with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6) as detector:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = detector.process(rgb)
        h, w = frame.shape[:2]

        name = "Bilinmiyor"

        if results.detections:
            for det in results.detections:
                bbox = det.location_data.relative_bounding_box
                x1 = max(0, int(bbox.xmin * w))
                y1 = max(0, int(bbox.ymin * h))
                x2 = min(w, int((bbox.xmin + bbox.width) * w))
                y2 = min(h, int((bbox.ymin + bbox.height) * h))

                face = frame[y1:y2, x1:x2]
                if face.size == 0:
                    continue

                gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (160,160))
                label, confidence = model.predict(gray)

                if confidence < 150:
                    name = inv_map.get(label, "Bilinmiyor")
                else:
                    name = "Bilinmiyor"

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame, name, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        #Tanıma güvenlik mantığı
        recent_names.append(name)
        current_time = time.time()

        # Aynı kişi 3 saniyede bir kaydedilebilir
        if name != "Bilinmiyor" and (name != last_seen_name or current_time - last_seen_time > 3):
            # Sadece eğer 10 karede 7 kez aynı isim görünürse emin ol
            if recent_names.count(name) > 7:
                current_servis = database.check_servis(name)
                if current_servis != "Bindi":
                    database.update_servis(name, "Bindi")
                    print(f"{name} kesin tanındı ve kaydedildi.")
                else:
                    print(f"{name} zaten geldi.")
                last_seen_name = name
                last_seen_time = current_time

        cv2.imshow("Canli Tanima - Akilli Sistem", frame)
        if cv2.waitKey(20) == 27:
            break

cap.release()
cv2.destroyAllWindows()
print("Program kapatıldı.")
