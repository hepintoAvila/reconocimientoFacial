import cv2
import sqlite3
import os
import sys

def capture_images(name):
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    conn = sqlite3.connect('data/faces.db')
    c = conn.cursor()

    # Verifica si la tabla de faces existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image_path TEXT
        )
    ''')

    os.makedirs('data/faces', exist_ok=True)
    
    count = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            file_path = f'data/faces/{name}_{count}.jpg'  # Concatenar nombre del usuario
            cv2.imwrite(file_path, face_img)
            c.execute("INSERT INTO faces (name, image_path) VALUES (?, ?)", (name, file_path))
            conn.commit()
        
        if count >= 30:  # Número de imágenes para capturar
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        user_name = sys.argv[1]
        capture_images(user_name)
    else:
        print('No name provided.')
