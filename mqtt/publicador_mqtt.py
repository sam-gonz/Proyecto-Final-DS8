"""
Publicador MQTT - Smart Home IoT
Script para enviar comandos de prueba al sistema
"""

import paho.mqtt.client as mqtt
import json
import ssl
import time
from datetime import datetime
from configuracion import MQTT_CONFIG, TOPICS

class PublicadorSmartHome:
    """Cliente MQTT para publicar comandos"""
    
    def __init__(self):
        """Inicializa el publicador"""
        self.cliente = mqtt.Client(client_id="control_escritorio")
        self.cliente.username_pw_set(MQTT_CONFIG["usuario"], MQTT_CONFIG["password"])
        
        # Configurar TLS/SSL
        if MQTT_CONFIG["usar_tls"]:
            self.cliente.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
        
        self.conectado = False
    
    def conectar(self):
        """Conecta al broker MQTT"""
        try:
            print("🔗 Conectando a broker MQTT...")
            self.cliente.connect(
                MQTT_CONFIG["broker"],
                MQTT_CONFIG["puerto"],
                MQTT_CONFIG["timeout"]
            )
            self.cliente.loop_start()
            time.sleep(2)  # Esperar conexión
            self.conectado = True
            print("✅ Conectado exitosamente\n")
            return True
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            return False
    
    def desconectar(self):
        """Desconecta del broker"""
        self.cliente.loop_stop()
        self.cliente.disconnect()
        print("✅ Desconectado")
    
    def publicar_comando(self, topic, comando):
        """
        Publica un comando en el topic especificado
        
        Args:
            topic: Topic MQTT
            comando: Diccionario con el comando
        """
        if not self.conectado:
            print("❌ No conectado al broker")
            return False
        
        try:
            payload = json.dumps(comando)
            result = self.cliente.publish(topic, payload, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"✅ [{timestamp}] Comando enviado: {comando}")
                return True
            else:
                print(f"❌ Error publicando comando. Código: {result.rc}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def encender_relay(self):
        """Envía comando para encender relay"""
        comando = {
            "dispositivo": "relay",
            "accion": "encender"
        }
        return self.publicar_comando(TOPICS["control"], comando)
    
    def apagar_relay(self):
        """Envía comando para apagar relay"""
        comando = {
            "dispositivo": "relay",
            "accion": "apagar"
        }
        return self.publicar_comando(TOPICS["control"], comando)
    
    def alternar_relay(self):
        """Envía comando para alternar relay"""
        comando = {
            "dispositivo": "relay",
            "accion": "alternar"
        }
        return self.publicar_comando(TOPICS["control"], comando)
    
    def cambiar_led(self, rojo, verde, azul):
        """
        Envía comando para cambiar color del LED
        
        Args:
            rojo: 0 o 1
            verde: 0 o 1
            azul: 0 o 1
        """
        comando = {
            "dispositivo": "led",
            "accion": "color",
            "r": rojo,
            "g": verde,
            "b": azul
        }
        return self.publicar_comando(TOPICS["control"], comando)
    
    def activar_buzzer(self):
        """Envía comando para activar buzzer"""
        comando = {
            "dispositivo": "buzzer",
            "accion": "encender"
        }
        return self.publicar_comando(TOPICS["control"], comando)
    
    def simular_datos_sensores(self, temperatura, humedad, movimiento=False):
        """
        Simula datos de sensores (útil para testing)
        
        Args:
            temperatura: Temperatura en °C
            humedad: Humedad en %
            movimiento: True/False
        """
        datos = {
            "temperatura": temperatura,
            "humedad": humedad,
            "movimiento": movimiento,
            "relay": False,
            "timestamp": time.time()
        }
        return self.publicar_comando(TOPICS["sensores"], datos)


def mostrar_menu():
    """Muestra el menú de opciones"""
    print("\n" + "=" * 60)
    print("🎛️  MENÚ DE CONTROL")
    print("=" * 60)
    print("1. Encender Relay (Ventilador/Luz)")
    print("2. Apagar Relay")
    print("3. Alternar Relay")
    print("4. LED Rojo")
    print("5. LED Verde")
    print("6. LED Azul")
    print("7. LED Apagado")
    print("8. Activar Buzzer")
    print("9. Simular datos de sensores")
    print("0. Salir")
    print("-" * 60)


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🏠 SMART HOME IOT - CONTROLADOR MQTT")
    print("   Universidad Tecnológica de Panamá")
    print("=" * 60 + "\n")
    
    publicador = PublicadorSmartHome()
    
    if not publicador.conectar():
        return
    
    try:
        while True:
            mostrar_menu()
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                publicador.encender_relay()
            
            elif opcion == "2":
                publicador.apagar_relay()
            
            elif opcion == "3":
                publicador.alternar_relay()
            
            elif opcion == "4":
                publicador.cambiar_led(1, 0, 0)
            
            elif opcion == "5":
                publicador.cambiar_led(0, 1, 0)
            
            elif opcion == "6":
                publicador.cambiar_led(0, 0, 1)
            
            elif opcion == "7":
                publicador.cambiar_led(0, 0, 0)
            
            elif opcion == "8":
                publicador.activar_buzzer()
            
            elif opcion == "9":
                try:
                    temp = float(input("Temperatura (°C): "))
                    hum = float(input("Humedad (%): "))
                    mov = input("Movimiento (s/n): ").lower() == 's'
                    publicador.simular_datos_sensores(temp, hum, mov)
                except ValueError:
                    print("❌ Valores inválidos")
            
            elif opcion == "0":
                print("\n👋 Saliendo...")
                break
            
            else:
                print("❌ Opción inválida")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Interrumpido por usuario")
    
    finally:
        publicador.desconectar()


if __name__ == "__main__":
    main()
