import cv2
import numpy as np
import sys
import signal

# Variable global para controlar el estado del script
running = True

def signal_handler(sig, frame):
    global running
    print('Exiting...')
    running = False
    cv2.destroyAllWindows()
    sys.exit(0)

def recognize_faces():
    # Cargar el modelo entrenado
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('models/trainer.yml')

    # Cargar el clasificador de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Iniciar la cámara
    cap = cv2.VideoCapture(0)

    while running:
        # Capturar frame por frame
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar caras en el frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id, confidence = recognizer.predict(roi_gray)
            
            # Ajusta el color del cuadro según la predicción
            if confidence < 70:  # Ajusta el umbral según sea necesario
                color = (0, 255, 0)  # Verde para rostro reconocido
            else:
                color = (0, 0, 255)  # Rojo para rostro no reconocido
            
            # Dibuja el cuadro alrededor de la cara
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Mostrar el frame
        cv2.imshow('Face Recognition', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

# Configura el manejador de señales para SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Ejecuta la función de reconocimiento de caras
recognize_faces()
