"""
Módulo de Utilidades
Funciones auxiliares del sistema
"""

import time

def imprimir_banner():
    """Imprime el banner inicial del sistema"""
    print("\n" + "=" * 60)
    print("🏠 SISTEMA SMART HOME IOT")
    print("   Raspberry Pi Pico W + MicroPython")
    print("   Universidad Tecnológica de Panamá")
    print("   Desarrollo de Software VIII")
    print("=" * 60 + "\n")

def imprimir_separador(texto=""):
    """Imprime un separador visual con texto opcional"""
    if texto:
        print(f"\n{'─' * 20} {texto} {'─' * 20}")
    else:
        print("─" * 60)

def formatear_tiempo(timestamp):
    """
    Formatea un timestamp a formato legible
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        str: Tiempo formateado
    """
    # MicroPython no tiene datetime, retornamos el timestamp
    return f"{int(timestamp)}"

def crear_mensaje_datos(temperatura, humedad, movimiento, relay_estado):
    """
    Crea un diccionario con datos del sistema
    
    Args:
        temperatura: Temperatura actual
        humedad: Humedad actual
        movimiento: Estado de movimiento
        relay_estado: Estado del relay
        
    Returns:
        dict: Datos formateados
    """
    return {
        "temperatura": round(temperatura, 2) if temperatura else None,
        "humedad": round(humedad, 2) if humedad else None,
        "movimiento": movimiento,
        "relay": relay_estado,
        "timestamp": time.time()
    }

def log_evento(tipo, mensaje):
    """
    Registra un evento en consola con formato
    
    Args:
        tipo: Tipo de evento (INFO, WARN, ERROR, etc.)
        mensaje: Mensaje a mostrar
    """
    iconos = {
        "INFO": "ℹ️",
        "WARN": "⚠️",
        "ERROR": "❌",
        "SUCCESS": "✅",
        "DATA": "📊"
    }
    icono = iconos.get(tipo, "📝")
    print(f"{icono} [{tipo}] {mensaje}")
