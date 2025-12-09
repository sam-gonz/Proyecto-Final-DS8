"""
Módulo de Sensores
Maneja la lectura de todos los sensores del sistema
"""

import dht
from machine import Pin
import time

class GestorSensores:
    """Clase para gestionar todos los sensores del sistema"""
    
    def __init__(self, pin_dht, pin_pir):
        """
        Inicializa los sensores
        
        Args:
            pin_dht: Pin GPIO para sensor DHT22
            pin_pir: Pin GPIO para sensor PIR
        """
        self.sensor_dht = dht.DHT22(Pin(pin_dht))
        self.sensor_pir = Pin(pin_pir, Pin.IN)
        
        # Variables para almacenar últimas lecturas
        self.temperatura = 0.0
        self.humedad = 0.0
        self.movimiento = False
        self.ultima_lectura_exitosa = 0
        
        print(" Sensores inicializados")
    
    def leer_temperatura_humedad(self):
        """
        Lee temperatura y humedad del sensor DHT22
        
        Returns:
            tuple: (temperatura, humedad) o (None, None) si hay error
        """
        try:
            self.sensor_dht.measure()
            self.temperatura = self.sensor_dht.temperature()
            self.humedad = self.sensor_dht.humidity()
            self.ultima_lectura_exitosa = time.time()
            return (self.temperatura, self.humedad)
        
        except OSError as e:
            print(f" Error leyendo DHT22: {e}")
            return (None, None)
    
    def leer_movimiento(self):
        """
        Lee el estado del sensor PIR
        
        Returns:
            bool: True si detecta movimiento, False si no
        """
        self.movimiento = self.sensor_pir.value() == 1
        return self.movimiento
    
    def leer_todos(self):
        """
        Lee todos los sensores del sistema
        
        Returns:
            dict: Diccionario con todas las lecturas
        """
        temp, hum = self.leer_temperatura_humedad()
        mov = self.leer_movimiento()
        
        return {
            "temperatura": temp,
            "humedad": hum,
            "movimiento": mov,
            "timestamp": time.time()
        }
    
    def obtener_ultima_temperatura(self):
        """Retorna la última temperatura leída"""
        return self.temperatura
    
    def obtener_ultima_humedad(self):
        """Retorna la última humedad leída"""
        return self.humedad
    
    def obtener_estado_movimiento(self):
        """Retorna el último estado de movimiento"""
        return self.movimiento
    
    def mostrar_lecturas(self):
        """Imprime las lecturas actuales en consola de forma formateada"""
        print(f" Temp: {self.temperatura:.1f}°C | Humedad: {self.humedad:.1f}% | Movimiento: {'SÍ' if self.movimiento else 'NO'}")
