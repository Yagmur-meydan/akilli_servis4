from flask import Flask, render_template, Response, redirect, url_for
import cv2
import mediapipe as mp
import numpy as np
import pickle
import database
import sqlite3
import time
from flask import jsonify

app = Flask(__name__)

# Model Yükle 
model = cv2.face.LBPHFaceRecognizer_create()
model.read("lbph_model.yml")
with open("label_map.pkl", "rb") as f:
    inv_map = pickle.load(f)

mp_face = mp.solutions.face_detection
cap = cv2.VideoCapture(0)

# Son görülen kişi için kontrol değişkenleri
last_seen_name = None
last_seen_time = 0

def gen_frames():
    global last_seen_name, last_seen_time

    with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6) as detector:
        while True:
            success, frame = cap.read()
            if not success:
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

                    # Veritabanı güncelleme (spam önleme ile)
                    current_time = time.time()
                    if name != "Bilinmiyor" and (name != last_seen_name or current_time - last_seen_time > 3):
                        current_servis = database.check_servis(name)
                        if current_servis != "Bindi":
                            database.update_servis(name, "Bindi")
                        last_seen_name = name
                        last_seen_time = current_time

                    # Görsel üzerine çizim
                    color = (0,255,0) if name != "Bilinmiyor" else (0,0,255)
                    cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
                    cv2.putText(frame, name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Görüntüyü web için encode et
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    students = database.list_students()
    return render_template('index.html', students=students)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/data')
def data():
    import sqlite3
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, servis, saat FROM students")
    students = cursor.fetchall()
    conn.close()
    return jsonify(students)
    
@app.route('/reset')
def reset():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET servis='Yok'")
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
