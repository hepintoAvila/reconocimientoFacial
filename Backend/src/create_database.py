import sqlite3
import os

def create_database():
    # Asegúrate de que el directorio existe
    os.makedirs(os.path.dirname('data/faces.db'), exist_ok=True)
    
    conn = sqlite3.connect('data/faces.db')
    c = conn.cursor()

    # Crear tabla de faces
    c.execute('''
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image_path TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_database()
