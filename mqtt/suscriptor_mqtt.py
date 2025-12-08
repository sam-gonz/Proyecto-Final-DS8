"""
Suscriptor MQTT con MySQL
Recibe datos del ESP32 via MQTT y guarda en MySQL
"""
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import json
import ssl

# Configuracion MQTT
BROKER = "smarthome-utp-310d528f.a02.usw2.aws.hivemq.cloud"
PORT = 8883
USERNAME = "esp32_client"
PASSWORD = "proyectoDS8"

TOPICS = [
    "smarthome/sensores",
    "smarthome/alertas",
    "smarthome/control"
]

# Configuracion MySQL
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # ← CAMBIA ESTO
    "database": "smart_home_db"
}

def conectar_mysql():
    """Conecta a MySQL"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"Conectado a MySQL: {MYSQL_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        exit(1)

db_conn = conectar_mysql()

def on_connect(client, userdata, flags, rc):
    """Callback al conectar"""
    if rc == 0:
        print("Conectado a HiveMQ Cloud")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"  Suscrito a: {topic}")
    else:
        print(f"Error de conexion MQTT: {rc}")

def on_message(client, userdata, msg):
    """Callback al recibir mensaje"""
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        
        print(f"\n{'='*50}")
        print(f"Topic: {topic}")
        print(f"Datos: {payload}")
        
        # Parsear JSON
        try:
            data = json.loads(payload)
        except:
            data = {"raw": payload}
        
        cursor = db_conn.cursor()
        
        # Guardar segun topic
        if topic == "smarthome/sensores":
            cursor.execute('''
                INSERT INTO lecturas_sensores 
                (temperatura, humedad, movimiento, relay_estado)
                VALUES (%s, %s, %s, %s)
            ''', (
                data.get("temperatura"),
                data.get("humedad"),
                1 if data.get("movimiento") else 0,
                1 if data.get("relay_estado") else 0
            ))
            print("GUARDADO en lecturas_sensores")
            
        elif topic == "smarthome/alertas":
            cursor.execute('''
                INSERT INTO eventos 
                (tipo, descripcion, ubicacion)
                VALUES (%s, %s, %s)
            ''', (
                data.get("tipo", "alerta"),
                json.dumps(data),
                data.get("ubicacion", "desconocida")
            ))
            print("GUARDADO en eventos")
            
        elif topic == "smarthome/control":
            cursor.execute('''
                INSERT INTO comandos 
                (comando, parametros)
                VALUES (%s, %s)
            ''', (
                data.get("comando", payload),
                json.dumps(data)
            ))
            print("GUARDADO en comandos")
        
        db_conn.commit()
        print(f"{'='*50}\n")
        
    except Error as e:
        print(f"Error MySQL: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect
client.on_message = on_message

# Conectar
print("\nConectando a HiveMQ Cloud...")
try:
    client.connect(BROKER, PORT, 60)
    print("Escuchando mensajes MQTT y guardando en MySQL...")
    print("Presiona Ctrl+C para detener\n")
    client.loop_forever()
    
except KeyboardInterrupt:
    print("\nDetenido por usuario")
    db_conn.close()
except Exception as e:
    print(f"Error: {e}")
    if db_conn:
        db_conn.close()
