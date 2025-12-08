"""
Gestor de Base de Datos - Smart Home IoT
Script Python para interactuar con la base de datos desde el escritorio
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json

class GestorBaseDatos:
    """Clase para gestionar conexiones y operaciones con la base de datos"""
    
    def __init__(self, host='localhost', usuario='root', password='', base_datos='smarthome_iot'):
        """
        Inicializa el gestor de base de datos
        
        Args:
            host: Host del servidor MySQL
            usuario: Usuario de MySQL
            password: Contraseña de MySQL
            base_datos: Nombre de la base de datos
        """
        self.host = host
        self.usuario = usuario
        self.password = password
        self.base_datos = base_datos
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.password,
                database=self.base_datos
            )
            
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor(dictionary=True)
                print(f"✅ Conectado a base de datos: {self.base_datos}")
                return True
        except Error as e:
            print(f"❌ Error conectando a MySQL: {e}")
            return False
    
    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        if self.cursor:
            self.cursor.close()
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("✅ Desconectado de la base de datos")
    
    def insertar_lectura(self, temperatura, humedad):
        """
        Inserta una lectura de sensores
        
        Args:
            temperatura: Temperatura en °C
            humedad: Humedad en %
        """
        try:
            query = """
            INSERT INTO lecturas_sensores (temperatura, humedad)
            VALUES (%s, %s)
            """
            self.cursor.execute(query, (temperatura, humedad))
            self.conexion.commit()
            print(f"📊 Lectura insertada: {temperatura}°C, {humedad}%")
            return True
        except Error as e:
            print(f"❌ Error insertando lectura: {e}")
            return False
    
    def registrar_movimiento(self, temperatura=None, humedad=None):
        """
        Registra un evento de movimiento
        
        Args:
            temperatura: Temperatura al momento del evento (opcional)
            humedad: Humedad al momento del evento (opcional)
        """
        try:
            query = """
            INSERT INTO eventos_movimiento (detectado, temperatura_momento, humedad_momento)
            VALUES (TRUE, %s, %s)
            """
            self.cursor.execute(query, (temperatura, humedad))
            self.conexion.commit()
            print("🚨 Evento de movimiento registrado")
            return True
        except Error as e:
            print(f"❌ Error registrando movimiento: {e}")
            return False
    
    def registrar_comando(self, dispositivo, accion, origen='manual', parametros=None):
        """
        Registra un comando ejecutado
        
        Args:
            dispositivo: Nombre del dispositivo
            accion: Acción ejecutada
            origen: Origen del comando
            parametros: Parámetros adicionales (dict)
        """
        try:
            parametros_json = json.dumps(parametros) if parametros else None
            
            query = """
            INSERT INTO comandos_control (dispositivo, accion, origen, parametros)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (dispositivo, accion, origen, parametros_json))
            self.conexion.commit()
            print(f"🎛️ Comando registrado: {dispositivo} -> {accion}")
            return True
        except Error as e:
            print(f"❌ Error registrando comando: {e}")
            return False
    
    def obtener_lecturas_recientes(self, limite=50):
        """
        Obtiene las lecturas más recientes
        
        Args:
            limite: Número de lecturas a obtener
            
        Returns:
            list: Lista de lecturas
        """
        try:
            query = """
            SELECT id, temperatura, humedad, fecha_hora
            FROM lecturas_sensores
            ORDER BY fecha_hora DESC
            LIMIT %s
            """
            self.cursor.execute(query, (limite,))
            resultados = self.cursor.fetchall()
            return resultados
        except Error as e:
            print(f"❌ Error obteniendo lecturas: {e}")
            return []
    
    def obtener_estadisticas_dia(self):
        """Obtiene estadísticas del día actual"""
        try:
            self.cursor.callproc('sp_estadisticas_dia')
            
            resultados = []
            for result in self.cursor.stored_results():
                resultados.append(result.fetchall())
            
            return resultados
        except Error as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return None
    
    def crear_alerta(self, tipo, severidad, mensaje, datos_contexto=None):
        """
        Crea una alerta en el sistema
        
        Args:
            tipo: Tipo de alerta
            severidad: 'info', 'advertencia', 'critica'
            mensaje: Mensaje de la alerta
            datos_contexto: Datos adicionales (dict)
        """
        try:
            contexto_json = json.dumps(datos_contexto) if datos_contexto else None
            
            query = """
            INSERT INTO alertas_sistema (tipo_alerta, severidad, mensaje, datos_contexto)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (tipo, severidad, mensaje, contexto_json))
            self.conexion.commit()
            print(f"🚨 Alerta creada: {tipo} - {severidad}")
            return True
        except Error as e:
            print(f"❌ Error creando alerta: {e}")
            return False


# ============================================================
# FUNCIONES DE TESTING
# ============================================================

def test_conexion():
    """Prueba la conexión a la base de datos"""
    print("\n" + "="*60)
    print("PROBANDO CONEXIÓN A BASE DE DATOS")
    print("="*60)
    
    # ACTUALIZAR ESTAS CREDENCIALES CON LAS TUYAS
    gestor = GestorBaseDatos(
        host='localhost',
        usuario='root',
        password='',  # Tu contraseña de MySQL
        base_datos='smarthome_iot'
    )
    
    if gestor.conectar():
        # Probar inserción de datos
        gestor.insertar_lectura(25.5, 60.0)
        gestor.registrar_movimiento(25.5, 60.0)
        gestor.registrar_comando('relay', 'encender', 'automatico')
        
        # Obtener lecturas recientes
        print("\n📊 Últimas 5 lecturas:")
        lecturas = gestor.obtener_lecturas_recientes(5)
        for lectura in lecturas:
            print(f"   {lectura['fecha_hora']}: {lectura['temperatura']}°C, {lectura['humedad']}%")
        
        gestor.desconectar()


if __name__ == "__main__":
    test_conexion()
