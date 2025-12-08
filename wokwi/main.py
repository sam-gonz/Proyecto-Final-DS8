"""
Programa Principal - Smart Home IoT
Raspberry Pi Pico W

Este archivo orquesta todos los módulos del sistema
"""

import time
import ujson
from configuracion import *
from sensores import GestorSensores
from actuadores import GestorActuadores
from conectividad import GestorConectividad
from automatizacion import GestorAutomatizacion
from utilidades import *

# ==================== VARIABLES GLOBALES ====================

# Gestores del sistema
gestor_sensores = None
gestor_actuadores = None
gestor_conectividad = None
gestor_automatizacion = None

# Contador de ciclos
contador_ciclos = 0

# ==================== CALLBACKS ====================

def callback_mqtt(topic, msg):
    """
    Callback para procesar mensajes MQTT entrantes
    
    Args:
        topic: Topic del mensaje
        msg: Contenido del mensaje
    """
    global gestor_actuadores
    
    log_evento("INFO", f"Mensaje MQTT recibido en {topic.decode()}")
    
    try:
        comando = ujson.loads(msg)
        dispositivo = comando.get("dispositivo", "")
        accion = comando.get("accion", "")
        
        if dispositivo == "relay":
            if accion == "encender":
                gestor_actuadores.activar_relay()
                log_evento("SUCCESS", "Relay activado remotamente")
            elif accion == "apagar":
                gestor_actuadores.desactivar_relay()
                log_evento("SUCCESS", "Relay desactivado remotamente")
            elif accion == "alternar":
                gestor_actuadores.alternar_relay()
                log_evento("SUCCESS", "Relay alternado remotamente")
        
        elif dispositivo == "led":
            r = comando.get("r", 0)
            g = comando.get("g", 0)
            b = comando.get("b", 0)
            gestor_actuadores.establecer_color_led(r, g, b)
            log_evento("SUCCESS", f"LED cambiado a RGB({r},{g},{b})")
        
        elif dispositivo == "buzzer":
            if accion == "encender":
                gestor_actuadores.activar_buzzer(0.5)
                log_evento("SUCCESS", "Buzzer activado remotamente")
        
        else:
            log_evento("WARN", f"Dispositivo desconocido: {dispositivo}")
    
    except Exception as e:
        log_evento("ERROR", f"Error procesando comando MQTT: {e}")

# ==================== FUNCIONES PRINCIPALES ====================

def inicializar_sistema():
    """Inicializa todos los componentes del sistema"""
    global gestor_sensores, gestor_actuadores, gestor_conectividad, gestor_automatizacion
    
    imprimir_banner()
    log_evento("INFO", "Iniciando sistema...")
    
    # Inicializar sensores
    imprimir_separador("SENSORES")
    gestor_sensores = GestorSensores(
        pin_dht=PINES["dht"],
        pin_pir=PINES["pir"]
    )
    
    # Inicializar actuadores
    imprimir_separador("ACTUADORES")
    gestor_actuadores = GestorActuadores(
        pin_relay=PINES["relay"],
        pin_led_r=PINES["led_rojo"],
        pin_led_g=PINES["led_verde"],
        pin_led_b=PINES["led_azul"],
        pin_buzzer=PINES["buzzer"]
    )
    
    # Estado inicial - LED azul (inicializando)
    gestor_actuadores.led_azul_encender()
    
    # Inicializar conectividad
    imprimir_separador("CONECTIVIDAD")
    config_wifi = {
        "ssid": WIFI_SSID,
        "password": WIFI_PASSWORD
    }
    gestor_conectividad = GestorConectividad(
        config_wifi=config_wifi,
        config_mqtt=CONFIGURACION_MQTT,
        callback_mensajes=callback_mqtt
    )
    
    # Conectar WiFi
    if not gestor_conectividad.conectar_wifi():
        log_evento("WARN", "Sistema continuando sin WiFi")
        gestor_actuadores.led_amarillo_encender()
        time.sleep(2)
    
    # Conectar MQTT
    if gestor_conectividad.conectado_wifi:
        topics_suscribir = [TOPICS_MQTT["control"]]
        if not gestor_conectividad.conectar_mqtt(topics_suscribir):
            log_evento("WARN", "Sistema continuando sin MQTT")
    
    # Inicializar automatización
    imprimir_separador("AUTOMATIZACIÓN")
    gestor_automatizacion = GestorAutomatizacion(
        gestor_sensores=gestor_sensores,
        gestor_actuadores=gestor_actuadores,
        parametros=PARAMETROS
    )
    
    # Sistema listo - LED verde
    gestor_actuadores.led_verde_encender()
    gestor_actuadores.buzzer_confirmacion()
    
    imprimir_separador()
    log_evento("SUCCESS", "Sistema inicializado correctamente")
    print("\n🚀 Iniciando loop principal...\n")

def ejecutar_loop_principal():
    """Loop principal del sistema"""
    global contador_ciclos
    
    while True:
        try:
            imprimir_separador(f"CICLO #{contador_ciclos + 1}")
            
            # 1. Leer sensores
            lecturas = gestor_sensores.leer_todos()
            
            if lecturas["temperatura"] is not None:
                gestor_sensores.mostrar_lecturas()
                
                # 2. Ejecutar automatización
                gestor_automatizacion.ejecutar_ciclo_automatico(
                    conectividad=gestor_conectividad,
                    topic_alertas=TOPICS_MQTT["alertas"]
                )
                
                # 3. Enviar datos por MQTT periódicamente
                if gestor_conectividad.conectado_mqtt and (contador_ciclos % PARAMETROS["intervalo_envio_mqtt"] == 0):
                    mensaje = crear_mensaje_datos(
                        temperatura=gestor_sensores.obtener_ultima_temperatura(),
                        humedad=gestor_sensores.obtener_ultima_humedad(),
                        movimiento=gestor_sensores.obtener_estado_movimiento(),
                        relay_estado=gestor_actuadores.obtener_estado_relay()
                    )
                    gestor_conectividad.publicar_mensaje(TOPICS_MQTT["sensores"], mensaje)
                    
                    # Verificar mensajes entrantes
                    gestor_conectividad.verificar_mensajes()
                
                # 4. Mostrar estado de actuadores
                gestor_actuadores.mostrar_estado()
            
            else:
                log_evento("WARN", "No se pudieron leer los sensores")
            
            contador_ciclos += 1
            time.sleep(PARAMETROS["intervalo_lectura"])
            
        except KeyboardInterrupt:
            log_evento("INFO", "Sistema detenido por usuario")
            break
        
        except Exception as e:
            log_evento("ERROR", f"Error en loop principal: {e}")
            gestor_actuadores.led_rojo_encender()
            time.sleep(5)
            gestor_actuadores.led_verde_encender()

def limpiar_y_finalizar():
    """Limpia recursos y finaliza el sistema"""
    print("\n")
    imprimir_separador("FINALIZANDO SISTEMA")
    
    log_evento("INFO", "Limpiando recursos...")
    
    # Desconectar MQTT
    if gestor_conectividad:
        gestor_conectividad.desconectar_mqtt()
    
    # Apagar actuadores
    if gestor_actuadores:
        gestor_actuadores.apagar_todo()
    
    imprimir_separador()
    log_evento("SUCCESS", "Sistema finalizado correctamente")
    print("=" * 60 + "\n")

# ==================== PUNTO DE ENTRADA ====================

def main():
    """Función principal del programa"""
    try:
        # Inicializar sistema
        inicializar_sistema()
        
        # Ejecutar loop principal
        ejecutar_loop_principal()
        
    finally:
        # Siempre limpiar al salir
        limpiar_y_finalizar()

# Ejecutar programa
if __name__ == "__main__":
    main()
