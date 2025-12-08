"""
Módulo de Conectividad
Maneja conexiones WiFi y MQTT
"""

import network
import time
from umqtt.simple import MQTTClient
import ujson

class GestorConectividad:
    """Clase para gestionar WiFi y MQTT"""
    
    def __init__(self, config_wifi, config_mqtt, callback_mensajes=None):
        """
        Inicializa el gestor de conectividad
        
        Args:
            config_wifi: Dict con ssid y password
            config_mqtt: Dict con configuración MQTT
            callback_mensajes: Función callback para mensajes MQTT
        """
        self.ssid = config_wifi["ssid"]
        self.password = config_wifi["password"]
        
        self.mqtt_broker = config_mqtt["broker"]
        self.mqtt_puerto = config_mqtt["puerto"]
        self.mqtt_usuario = config_mqtt["usuario"]
        self.mqtt_password = config_mqtt["password"]
        self.mqtt_cliente_id = config_mqtt["cliente_id"]
        self.mqtt_keepalive = config_mqtt.get("keepalive", 7200)
        
        self.wlan = None
        self.cliente_mqtt = None
        self.callback_mensajes = callback_mensajes
        self.conectado_wifi = False
        self.conectado_mqtt = False
        
        print("✅ Gestor de conectividad inicializado")
    
    def conectar_wifi(self, timeout=10):
        """
        Conecta a la red WiFi
        
        Args:
            timeout: Tiempo máximo de espera en segundos
            
        Returns:
            bool: True si conectó exitosamente, False si no
        """
        print("=" * 50)
        print(f"📡 Conectando a WiFi: {self.ssid}")
        print("=" * 50)
        
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        
        intentos = timeout
        while intentos > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            intentos -= 1
            print(f"   Esperando conexión... ({timeout - intentos}/{timeout})")
            time.sleep(1)
        
        if self.wlan.status() != 3:
            print("❌ Error: No se pudo conectar a WiFi")
            self.conectado_wifi = False
            return False
        else:
            status = self.wlan.ifconfig()
            print("✅ WiFi conectado exitosamente!")
            print(f"   📍 Dirección IP: {status[0]}")
            print(f"   📍 Máscara: {status[1]}")
            print(f"   📍 Gateway: {status[2]}")
            self.conectado_wifi = True
            return True
    
    def conectar_mqtt(self, topics_suscribir=[]):
        """
        Conecta al broker MQTT
        
        Args:
            topics_suscribir: Lista de topics para suscribirse
            
        Returns:
            bool: True si conectó exitosamente, False si no
        """
        print("\n" + "=" * 50)
        print("🔗 Conectando a broker MQTT...")
        print(f"   Broker: {self.mqtt_broker}")
        print(f"   Puerto: {self.mqtt_puerto}")
        print("=" * 50)
        
        try:
            self.cliente_mqtt = MQTTClient(
                client_id=self.mqtt_cliente_id,
                server=self.mqtt_broker,
                port=self.mqtt_puerto,
                user=self.mqtt_usuario,
                password=self.mqtt_password,
                keepalive=self.mqtt_keepalive,
                ssl=True,
                ssl_params={'server_hostname': self.mqtt_broker}
            )
            
            if self.callback_mensajes:
                self.cliente_mqtt.set_callback(self.callback_mensajes)
            
            self.cliente_mqtt.connect()
            print("✅ Conectado a broker MQTT exitosamente!")
            
            # Suscribirse a topics
            for topic in topics_suscribir:
                self.cliente_mqtt.subscribe(topic)
                print(f"   📬 Suscrito a: {topic}")
            
            self.conectado_mqtt = True
            return True
            
        except Exception as e:
            print(f"❌ Error conectando a MQTT: {e}")
            self.conectado_mqtt = False
            return False
    
    def publicar_mensaje(self, topic, datos):
        """
        Publica un mensaje en un topic MQTT
        
        Args:
            topic: Topic MQTT
            datos: Diccionario con datos a enviar
            
        Returns:
            bool: True si se publicó exitosamente
        """
        if not self.conectado_mqtt or not self.cliente_mqtt:
            print("⚠️ No conectado a MQTT, no se puede publicar")
            return False
        
        try:
            payload = ujson.dumps(datos)
            self.cliente_mqtt.publish(topic, payload)
            print(f"📤 Mensaje publicado en {topic}")
            return True
        except Exception as e:
            print(f"❌ Error publicando mensaje: {e}")
            return False
    
    def verificar_mensajes(self):
        """Verifica si hay mensajes MQTT entrantes"""
        if self.conectado_mqtt and self.cliente_mqtt:
            try:
                self.cliente_mqtt.check_msg()
            except Exception as e:
                print(f"⚠️ Error verificando mensajes: {e}")
    
    def desconectar_mqtt(self):
        """Desconecta del broker MQTT"""
        if self.cliente_mqtt:
            try:
                self.cliente_mqtt.disconnect()
                print("✅ Desconectado de MQTT")
            except:
                pass
        self.conectado_mqtt = False
    
    def desconectar_wifi(self):
        """Desconecta del WiFi"""
        if self.wlan:
            self.wlan.active(False)
            print("✅ Desconectado de WiFi")
        self.conectado_wifi = False
    
    def esta_conectado(self):
        """
        Verifica si está conectado a WiFi y MQTT
        
        Returns:
            tuple: (wifi_conectado, mqtt_conectado)
        """
        return (self.conectado_wifi, self.conectado_mqtt)
