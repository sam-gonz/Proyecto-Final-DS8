"""
Suscriptor MQTT - Smart Home IoT
Script para monitorear todos los mensajes del sistema desde el escritorio
"""

import paho.mqtt.client as mqtt
import json
import ssl
from datetime import datetime
from configuracion import MQTT_CONFIG, TOPICS

class SuscriptorSmartHome:
    """Cliente MQTT para suscribirse y monitorear mensajes"""
    
    def __init__(self):
        """Inicializa el suscriptor"""
        self.cliente = mqtt.Client(client_id="monitor_escritorio")
        self.cliente.username_pw_set(MQTT_CONFIG["usuario"], MQTT_CONFIG["password"])
        
        # Configurar TLS/SSL
        if MQTT_CONFIG["usar_tls"]:
            self.cliente.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
        
        # Callbacks
        self.cliente.on_connect = self.on_connect
        self.cliente.on_message = self.on_message
        self.cliente.on_disconnect = self.on_disconnect
        
        self.conectado = False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback cuando se conecta al broker"""
        if rc == 0:
            print("=" * 70)
            print("✅ CONECTADO A BROKER MQTT")
            print(f"   Broker: {MQTT_CONFIG['broker']}")
            print(f"   Puerto: {MQTT_CONFIG['puerto']}")
            print("=" * 70)
            self.conectado = True
            
            # Suscribirse a todos los topics
            print("\n📬 Suscribiéndose a topics:")
            for nombre, topic in TOPICS.items():
                self.cliente.subscribe(topic)
                print(f"   ✓ {topic}")
            
            print("\n🔍 Monitoreando mensajes... (Ctrl+C para salir)\n")
            print("-" * 70)
        else:
            print(f"❌ Error de conexión. Código: {rc}")
            self.conectado = False
    
    def on_message(self, client, userdata, msg):
        """Callback cuando llega un mensaje"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topic = msg.topic
        
        try:
            # Intentar decodificar como JSON
            payload = json.loads(msg.payload.decode())
            
            print(f"\n📨 MENSAJE RECIBIDO [{timestamp}]")
            print(f"   Topic: {topic}")
            print(f"   Datos:")
            
            # Formatear según el topic
            if topic == TOPICS["sensores"]:
                print(f"      🌡️  Temperatura: {payload.get('temperatura', 'N/A')}°C")
                print(f"      💧 Humedad: {payload.get('humedad', 'N/A')}%")
                print(f"      🚶 Movimiento: {'SÍ' if payload.get('movimiento') else 'NO'}")
                print(f"      🔌 Relay: {'ON' if payload.get('relay') else 'OFF'}")
            
            elif topic == TOPICS["alertas"]:
                print(f"      🚨 Tipo: {payload.get('tipo', 'N/A')}")
                print(f"      🌡️  Temperatura: {payload.get('temperatura', 'N/A')}°C")
                print(f"      💧 Humedad: {payload.get('humedad', 'N/A')}%")
            
            elif topic == TOPICS["control"]:
                print(f"      🎛️  Dispositivo: {payload.get('dispositivo', 'N/A')}")
                print(f"      ⚙️  Acción: {payload.get('accion', 'N/A')}")
            
            else:
                # Mostrar JSON completo
                for key, value in payload.items():
                    print(f"      {key}: {value}")
            
            print("-" * 70)
            
        except json.JSONDecodeError:
            # Si no es JSON, mostrar payload directo
            print(f"\n📨 MENSAJE [{timestamp}]")
            print(f"   Topic: {topic}")
            print(f"   Payload: {msg.payload.decode()}")
            print("-" * 70)
    
    def on_disconnect(self, client, userdata, rc):
        """Callback cuando se desconecta"""
        print("\n⚠️  Desconectado del broker")
        self.conectado = False
    
    def conectar(self):
        """Conecta al broker MQTT"""
        try:
            print("\n🔗 Conectando a broker MQTT...")
            self.cliente.connect(
                MQTT_CONFIG["broker"],
                MQTT_CONFIG["puerto"],
                MQTT_CONFIG["timeout"]
            )
            return True
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            return False
    
    def iniciar(self):
        """Inicia el loop de escucha"""
        if self.conectar():
            try:
                self.cliente.loop_forever()
            except KeyboardInterrupt:
                print("\n\n⛔ Deteniendo monitor...")
                self.cliente.disconnect()
                print("✅ Monitor detenido correctamente")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🏠 SMART HOME IOT - MONITOR MQTT")
    print("   Universidad Tecnológica de Panamá")
    print("=" * 70)
    
    monitor = SuscriptorSmartHome()
    monitor.iniciar()


if __name__ == "__main__":
    main()
