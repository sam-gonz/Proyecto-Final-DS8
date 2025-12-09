"""
Gestor de Base de Datos - MySQL
Crea y gestiona la base de datos del Smart Home
"""
import mysql.connector
from mysql.connector import Error

# Configuracion MySQL
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "smart_home_db"
}

def crear_base_datos():
    """Crea la base de datos y tablas en MySQL"""
    try:
        # Conectar sin especificar base de datos
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"]
        )
        
        cursor = conn.cursor()
        
        # Crear base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        print(f"Base de datos '{MYSQL_CONFIG['database']}' creada/verificada")
        
        # Usar la base de datos
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        
        # Tabla de lecturas de sensores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecturas_sensores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temperatura FLOAT,
                humedad FLOAT,
                movimiento TINYINT(1),
                relay_estado TINYINT(1)
            )
        ''')
        print("Tabla 'lecturas_sensores' creada")
        
        # Tabla de eventos/alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo VARCHAR(50),
                descripcion TEXT,
                ubicacion VARCHAR(100)
            )
        ''')
        print("Tabla 'eventos' creada")
        
        # Tabla de comandos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comandos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                comando VARCHAR(100),
                parametros TEXT,
                ejecutado TINYINT(1) DEFAULT 0
            )
        ''')
        print("Tabla 'comandos' creada")
        
        conn.commit()
        print("\nBase de datos MySQL configurada correctamente")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        print("\nSoluciones:")
        print("1. Verifica que MySQL este corriendo")
        print("2. Cambia la password en MYSQL_CONFIG")
        print("3. Si no tienes password, usa: password=''")

def verificar_base_datos():
    """Verifica contenido de la BD"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM lecturas_sensores")
        lecturas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM eventos")
        eventos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM comandos")
        comandos = cursor.fetchone()[0]
        
        print(f"\nEstadisticas de la base de datos:")
        print(f"  Lecturas guardadas: {lecturas}")
        print(f"  Eventos guardados: {eventos}")
        print(f"  Comandos guardados: {comandos}")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error verificando BD: {e}")

if __name__ == "__main__":
    print("Inicializando base de datos MySQL...")
    print("="*50)
    crear_base_datos()
    verificar_base_datos()
