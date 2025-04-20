
import os
import sqlite3

# Calcular la ruta absoluta al archivo pos_system.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "pos_system.db")

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Crear tabla de clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        telefono TEXT,
        credito REAL
    )''')

    # Crear tabla de inventario
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        cantidad INTEGER,
        precio REAL
    )''')

    # Crear tabla de ventas
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        fecha TEXT,
        total REAL,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )''')

    # Crear tabla de usuarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        password TEXT,
        rol TEXT
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✔ Base de datos y tablas creadas correctamente.")
