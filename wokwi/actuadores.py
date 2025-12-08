"""
Módulo de Actuadores
Controla todos los actuadores del sistema (relay, LEDs, buzzer)
"""

from machine import Pin
import time

class GestorActuadores:
    """Clase para gestionar todos los actuadores del sistema"""
    
    def __init__(self, pin_relay, pin_led_r, pin_led_g, pin_led_b, pin_buzzer):
        """
        Inicializa los actuadores
        
        Args:
            pin_relay: Pin GPIO para relay
            pin_led_r: Pin GPIO para LED rojo
            pin_led_g: Pin GPIO para LED verde
            pin_led_b: Pin GPIO para LED azul
            pin_buzzer: Pin GPIO para buzzer
        """
        # Inicializar pines como salida
        self.relay = Pin(pin_relay, Pin.OUT)
        self.led_rojo = Pin(pin_led_r, Pin.OUT)
        self.led_verde = Pin(pin_led_g, Pin.OUT)
        self.led_azul = Pin(pin_led_b, Pin.OUT)
        self.buzzer = Pin(pin_buzzer, Pin.OUT)
        
        # Estado actual
        self.relay_activo = False
        self.color_led_actual = (0, 0, 0)
        
        # Apagar todo al iniciar
        self.apagar_todo()
        
        print("✅ Actuadores inicializados")
    
    def activar_relay(self):
        """Activa el relay (enciende ventilador/luz)"""
        self.relay.value(1)
        self.relay_activo = True
        print("🔌 Relay ACTIVADO")
    
    def desactivar_relay(self):
        """Desactiva el relay (apaga ventilador/luz)"""
        self.relay.value(0)
        self.relay_activo = False
        print("🔌 Relay DESACTIVADO")
    
    def alternar_relay(self):
        """Alterna el estado del relay"""
        if self.relay_activo:
            self.desactivar_relay()
        else:
            self.activar_relay()
    
    def obtener_estado_relay(self):
        """Retorna el estado actual del relay"""
        return self.relay_activo
    
    def establecer_color_led(self, rojo, verde, azul):
        """
        Establece el color del LED RGB
        
        Args:
            rojo: 0 o 1
            verde: 0 o 1
            azul: 0 o 1
        """
        self.led_rojo.value(rojo)
        self.led_verde.value(verde)
        self.led_azul.value(azul)
        self.color_led_actual = (rojo, verde, azul)
    
    def led_rojo_encender(self):
        """LED rojo - Indica error o problema"""
        self.establecer_color_led(1, 0, 0)
    
    def led_verde_encender(self):
        """LED verde - Indica sistema OK"""
        self.establecer_color_led(0, 1, 0)
    
    def led_azul_encender(self):
        """LED azul - Indica inicialización"""
        self.establecer_color_led(0, 0, 1)
    
    def led_morado_encender(self):
        """LED morado - Indica alerta"""
        self.establecer_color_led(1, 0, 1)
    
    def led_amarillo_encender(self):
        """LED amarillo - Indica advertencia"""
        self.establecer_color_led(1, 1, 0)
    
    def led_apagar(self):
        """Apaga el LED RGB"""
        self.establecer_color_led(0, 0, 0)
    
    def activar_buzzer(self, duracion=0.5):
        """
        Activa el buzzer por un tiempo determinado
        
        Args:
            duracion: Duración en segundos (default: 0.5)
        """
        self.buzzer.value(1)
        time.sleep(duracion)
        self.buzzer.value(0)
    
    def buzzer_alerta(self):
        """Patrón de sonido para alerta (2 beeps cortos)"""
        self.activar_buzzer(0.2)
        time.sleep(0.1)
        self.activar_buzzer(0.2)
    
    def buzzer_error(self):
        """Patrón de sonido para error (beep largo)"""
        self.activar_buzzer(1.0)
    
    def buzzer_confirmacion(self):
        """Patrón de sonido para confirmación (beep muy corto)"""
        self.activar_buzzer(0.1)
    
    def apagar_todo(self):
        """Apaga todos los actuadores"""
        self.desactivar_relay()
        self.led_apagar()
        self.buzzer.value(0)
        print("🔕 Todos los actuadores apagados")
    
    def mostrar_estado(self):
        """Muestra el estado actual de los actuadores"""
        print(f"🎛️ Estado: Relay={'ON' if self.relay_activo else 'OFF'} | LED=RGB{self.color_led_actual}")
