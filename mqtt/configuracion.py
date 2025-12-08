"""
Configuración MQTT para scripts de escritorio
Smart Home IoT - Testing y Monitoreo
"""

# ==================== CONFIGURACIÓN HIVEMQ CLOUD ====================
# ACTUALIZAR CON TUS CREDENCIALES REALES
MQTT_CONFIG = {
    "broker": "smarthome-utp-310d528f.a02.usw2.aws.hivemq.cloud",  # Tu Cluster URL
    "puerto": 8883,
    "usuario": "esp32_client",                  # Tu usuario
    "password": "proyectoDS8",             # Tu password
    "usar_tls": True,
    "timeout": 60
}

# ==================== TOPICS ====================
TOPICS = {
    "sensores": "smarthome/sensores",
    "control": "smarthome/control",
    "alertas": "smarthome/alertas",
    "estado": "smarthome/estado"
}

# ==================== CONFIGURACIÓN DE TESTING ====================
TEST_CONFIG = {
    "intervalo_publicacion": 5,  # Segundos entre publicaciones de prueba
    "mostrar_timestamps": True,
    "guardar_log": True,
    "archivo_log": "mqtt_log.txt"
}
