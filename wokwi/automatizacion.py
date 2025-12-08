"""
Módulo de Automatización
Contiene la lógica de control automático del Smart Home
"""

import time

class GestorAutomatizacion:
    """Clase para gestionar la automatización del sistema"""
    
    def __init__(self, gestor_sensores, gestor_actuadores, parametros):
        """
        Inicializa el gestor de automatización
        
        Args:
            gestor_sensores: Instancia de GestorSensores
            gestor_actuadores: Instancia de GestorActuadores
            parametros: Dict con parámetros de control
        """
        self.sensores = gestor_sensores
        self.actuadores = gestor_actuadores
        
        self.temp_maxima = parametros["temp_maxima"]
        self.temp_minima = parametros["temp_minima"]
        self.cooldown_alerta = parametros["cooldown_alerta"]
        
        self.ultima_alerta_movimiento = 0
        
        print("✅ Gestor de automatización inicializado")
    
    def control_climatizacion(self):
        """
        Controla automáticamente el relay según la temperatura
        Sistema de histéresis para evitar oscilaciones
        """
        temperatura = self.sensores.obtener_ultima_temperatura()
        relay_activo = self.actuadores.obtener_estado_relay()
        
        # Temperatura muy alta → Activar ventilador
        if temperatura > self.temp_maxima and not relay_activo:
            print(f"🌡️ Temp alta ({temperatura:.1f}°C) → Activando ventilador")
            self.actuadores.activar_relay()
            return True
        
        # Temperatura normal → Desactivar ventilador
        elif temperatura < self.temp_minima and relay_activo:
            print(f"🌡️ Temp normal ({temperatura:.1f}°C) → Desactivando ventilador")
            self.actuadores.desactivar_relay()
            return True
        
        return False
    
    def procesar_alerta_movimiento(self, conectividad, topic_alertas):
        """
        Procesa detección de movimiento y genera alerta
        
        Args:
            conectividad: Instancia de GestorConectividad
            topic_alertas: Topic MQTT para alertas
            
        Returns:
            bool: True si se generó alerta
        """
        if not self.sensores.obtener_estado_movimiento():
            return False
        
        tiempo_actual = time.time()
        
        # Evitar spam de alertas
        if tiempo_actual - self.ultima_alerta_movimiento < self.cooldown_alerta:
            return False
        
        print("🚨 ¡ALERTA! Movimiento detectado")
        
        # Activar buzzer
        self.actuadores.buzzer_alerta()
        
        # LED morado temporalmente
        self.actuadores.led_morado_encender()
        time.sleep(0.3)
        self.actuadores.led_verde_encender()
        
        # Enviar alerta por MQTT
        if conectividad and conectividad.conectado_mqtt:
            datos_alerta = {
                "tipo": "movimiento",
                "timestamp": tiempo_actual,
                "temperatura": self.sensores.obtener_ultima_temperatura(),
                "humedad": self.sensores.obtener_ultima_humedad()
            }
            conectividad.publicar_mensaje(topic_alertas, datos_alerta)
        
        self.ultima_alerta_movimiento = tiempo_actual
        return True
    
    def ejecutar_ciclo_automatico(self, conectividad=None, topic_alertas=None):
        """
        Ejecuta un ciclo completo de automatización
        
        Args:
            conectividad: Instancia de GestorConectividad (opcional)
            topic_alertas: Topic para alertas (opcional)
            
        Returns:
            dict: Estado del ciclo ejecutado
        """
        # Control de climatización
        cambio_clima = self.control_climatizacion()
        
        # Procesar alertas de movimiento
        alerta_generada = False
        if conectividad and topic_alertas:
            alerta_generada = self.procesar_alerta_movimiento(conectividad, topic_alertas)
        
        return {
            "cambio_clima": cambio_clima,
            "alerta_generada": alerta_generada
        }
