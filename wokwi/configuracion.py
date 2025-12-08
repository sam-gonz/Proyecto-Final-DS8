"""
Configuración del Sistema Smart Home IoT
Raspberry Pi Pico W - MicroPython
Proyecto Final - Desarrollo de Software VIII
"""

# ==================== CONFIGURACIÓN WIFI ====================
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# ==================== CONFIGURACIÓN MQTT ====================
# ACTUALIZAR CON TUS CREDENCIALES DE HIVEMQ CLOUD
CONFIGURACION_MQTT = {
    "broker": "smarthome-utp-310d528f.a02.usw2.aws.hivemq.cloud",  # Ej: abc123xyz.s2.eu.hivemq.cloud
    "puerto": 8883,
    "usuario": "esp32_client",
    "password": "proyectoDS8",
    "cliente_id": "picow_smarthome",
    "keepalive": 7200,
    "usar_ssl": True
}

# Topics MQTT
TOPICS_MQTT = {
    "sensores": "smarthome/sensores",
    "control": "smarthome/control",
    "alertas": "smarthome/alertas",
    "estado": "smarthome/estado"
}

# ==================== PINES GPIO - RASPBERRY PI PICO W ====================
PINES = {
    "dht": 15,           # GPIO15 - Sensor DHT22 (Temp/Humedad)
    "pir": 14,           # GPIO14 - Sensor PIR (Movimiento)
    "relay": 12,         # GPIO12 - Módulo Relay
    "led_rojo": 16,      # GPIO16 - LED Rojo
    "led_verde": 17,     # GPIO17 - LED Verde
    "led_azul": 18,      # GPIO18 - LED Azul
    "buzzer": 13,        # GPIO13 - Buzzer
    "lcd_sda": 20,       # GPIO20 - Display LCD I2C SDA
    "lcd_scl": 21        # GPIO21 - Display LCD I2C SCL
}

# ==================== PARÁMETROS DEL SISTEMA ====================
PARAMETROS = {
    "temp_maxima": 28.0,           # °C - Activar ventilador
    "temp_minima": 25.0,           # °C - Desactivar ventilador
    "intervalo_lectura": 3,        # Segundos entre lecturas
    "intervalo_envio_mqtt": 10,    # Enviar datos cada X ciclos
    "cooldown_alerta": 5           # Segundos entre alertas de movimiento
}

CONFIGURACION_THINGSPEAK = {
    "api_key": "LTW26AZJYVJYKKT9",
    "canal_id": "3195638",
    "url": "https://api.thingspeak.com/update"
}
