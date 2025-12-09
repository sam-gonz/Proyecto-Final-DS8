# 🏠 Smart Home IoT – Sistema de Automatización  
Proyecto final de **Desarrollo de Software VIII – UTP**  
Sistema de domótica con **ESP32** para monitoreo en tiempo real de temperatura, humedad y movimiento.

---

## ✨ Características

- 🌡️ **Sensor DHT22** – Lectura de temperatura y humedad  
- 👀 **Sensor PIR** – Detección de movimiento  
- 🔌 **Control automático con relay**  
- 🌈 **Indicadores LED RGB**  
- 🖥️ **Display LCD I2C**  
- 🔊 **Alertas sonoras con buzzer**  
- ☁️ **Comunicación MQTT** (HiveMQ Cloud)  
- 📊 **Visualización en ThingSpeak**  
- 🗄️ **Almacenamiento en MySQL**

---

## 📁 Estructura del Proyecto



```txt
PROYECTO-FINAL-DS8/
|
|
├── database/                 # Base de datos MySQL
│   ├── consultas.sql         # Consultas SQL útiles
│   ├── esquema.sql           # Esquema de la base de datos
│   └── gestor_bd.py          # Script para crear/gestionar BD
|
├── documentacion/            # Documentación del proyecto
│   ├── arquitectura-iot.png
│   ├── arquitectura-sistema.md
│   ├── diagrama-flujo-datos.png
│   ├── manual-configuracion.md
│   └── manual-usuario.md
|
├── mqtt/                     # Scripts MQTT
│   ├── __pycache__/
│   └── suscriptor_mqtt.py    # Recibe datos MQTT y guarda en BD
|
├── wokwi/                    # Código ESP32 (MicroPython)
│   ├── capturas/             # Screenshots del proyecto
│   ├── actuadores.py         # Control de actuadores (relay, LED, buzzer, LCD)
│   ├── automatizacion.py     # Lógica de control automático
│   ├── conectividad.py       # Gestión de WiFi y MQTT
│   ├── configuracion.py      # Configuración del sistema
│   ├── diagram.json          # Configuración del circuito Wokwi
│   ├── main.py               # Programa principal
│   ├── sensores.py           # Gestión de sensores (DHT22, PIR)
│   └── utilidades.py         # Funciones auxiliares
|
├── README.md                 # Documentación principal
└── requirements.txt          # Dependencias Python
```
---

## ⚙️ Instalación

### 1️⃣ Clonar repositorio
  git clone https://github.com/sam-gonz/Proyecto-Final-DS8

### 2️⃣ Instalar dependencias Python
  pip install -r requirements.txt

3️⃣ Configurar base de datos
  cd database
  python gestor_bd.py

---

# 🔧 Configuración

## 1️⃣ MQTT (HiveMQ Cloud)

Editar el archivo: `wokwi/configuracion.py`

CONFIGURACION_MQTT = {
    "broker": "tu-cluster.hivemq.cloud",
    "puerto": 8883,
    "usuario": "tu_usuario",
    "password": "tu_password"
}

## 2️⃣ ThingSpeak
CONFIGURACION_THINGSPEAK = {
    "api_key": "TU_WRITE_API_KEY",
    "canal_id": "TU_CANAL_ID"
}

## 3️⃣ MySQL
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "tu_password_mysql",
    "database": "smart_home_db"
}
