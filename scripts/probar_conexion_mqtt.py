"""
Script de Diagnóstico - Prueba de Conexión MQTT
Verifica que todo esté configurado correctamente
"""

import paho.mqtt.client as mqtt
import ssl
import sys
import os
import time

# Agregar el directorio raíz al path
ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ruta_raiz)

try:
    from mqtt.configuracion import MQTT_CONFIG, TOPICS
except ImportError:
    print("❌ Error: No se puede importar configuracion.py")
    print("   Asegúrate de ejecutar desde la raíz del proyecto")
    sys.exit(1)

def probar_conexion():
    """Prueba la conexión al broker MQTT"""
    print("\n" + "=" * 70)
    print("🔍 DIAGNÓSTICO DE CONEXIÓN MQTT")
    print("=" * 70)
    
    print("\n📋 Configuración actual:")
    print(f"   Broker: {MQTT_CONFIG['broker']}")
    print(f"   Puerto: {MQTT_CONFIG['puerto']}")
    print(f"   Usuario: {MQTT_CONFIG['usuario']}")
    print(f"   TLS/SSL: {'Sí' if MQTT_CONFIG['usar_tls'] else 'No'}")
    
    print("\n🔗 Intentando conectar...")
    
    # Crear cliente
    cliente = mqtt.Client(client_id="test_conexion")
    cliente.username_pw_set(MQTT_CONFIG["usuario"], MQTT_CONFIG["password"])
    
    # Configurar TLS
    if MQTT_CONFIG["usar_tls"]:
        cliente.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    
    # Callbacks
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ CONEXIÓN EXITOSA")
            print("\n📬 Topics configurados:")
            for nombre, topic in TOPICS.items():
                print(f"   • {nombre}: {topic}")
        else:
            print(f"❌ CONEXIÓN FALLIDA. Código de error: {rc}")
            print("\nCódigos de error comunes:")
            print("   1: Versión de protocolo incorrecta")
            print("   2: Identificador rechazado")
            print("   3: Servidor no disponible")
            print("   4: Usuario o contraseña incorrectos")
            print("   5: No autorizado")
    
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print(f"⚠️  Desconexión inesperada. Código: {rc}")
    
    cliente.on_connect = on_connect
    cliente.on_disconnect = on_disconnect
    
    try:
        cliente.connect(MQTT_CONFIG["broker"], MQTT_CONFIG["puerto"], 60)
        cliente.loop_start()
        time.sleep(3)
        cliente.loop_stop()
        cliente.disconnect()
        
        print("\n" + "=" * 70)
        print("✅ DIAGNÓSTICO COMPLETADO")
        print("=" * 70 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Verifica:")
        print("   1. Credenciales en mqtt/configuracion.py")
        print("   2. Conexión a internet")
        print("   3. Cluster activo en HiveMQ Cloud")
        print("\n" + "=" * 70 + "\n")
        return False


if __name__ == "__main__":
    probar_conexion()
