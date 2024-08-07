import cv2
import numpy as np
import sqlite3

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    faces = []
    ids = []
    
    conn = sqlite3.connect('data/faces.db')
    c = conn.cursor()
    c.execute("SELECT * FROM faces")
    rows = c.fetchall()
    
    for row in rows:
        img = cv2.imread(row[2], 0)
        id = row[0]
        faces.append(img)
        ids.append(id)
    
    recognizer.train(faces, np.array(ids))
    recognizer.save('models/trainer.yml')
    
    conn.close()

train_model()
