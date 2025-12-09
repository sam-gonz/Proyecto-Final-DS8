
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS smarthome_iot
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE smarthome_iot;

-- TABLA: lecturas_sensores
-- Almacena todas las lecturas de temperatura y humedad

CREATE TABLE IF NOT EXISTS lecturas_sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura DECIMAL(5,2) NOT NULL COMMENT 'Temperatura en grados Celsius',
    humedad DECIMAL(5,2) NOT NULL COMMENT 'Humedad relativa en porcentaje',
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp de la lectura',
    INDEX idx_fecha_hora (fecha_hora),
    INDEX idx_temperatura (temperatura)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registro histórico de lecturas de sensores';

-- TABLA: eventos_movimiento
-- Registra detecciones de movimiento por el sensor PIR
CREATE TABLE IF NOT EXISTS eventos_movimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    detectado BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Indica si se detectó movimiento',
    temperatura_momento DECIMAL(5,2) COMMENT 'Temperatura al momento del evento',
    humedad_momento DECIMAL(5,2) COMMENT 'Humedad al momento del evento',
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp del evento',
    INDEX idx_fecha_hora (fecha_hora),
    INDEX idx_detectado (detectado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registro de eventos de detección de movimiento';

-- TABLA: comandos_control
-- Registra todos los comandos ejecutados en el sistema
CREATE TABLE IF NOT EXISTS comandos_control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dispositivo VARCHAR(50) NOT NULL COMMENT 'Nombre del dispositivo (relay, led, buzzer)',
    accion VARCHAR(50) NOT NULL COMMENT 'Acción ejecutada (encender, apagar, etc)',
    origen VARCHAR(50) DEFAULT 'manual' COMMENT 'Origen del comando (manual, automatico, mqtt)',
    parametros JSON COMMENT 'Parámetros adicionales del comando',
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp del comando',
    INDEX idx_dispositivo (dispositivo),
    INDEX idx_fecha_hora (fecha_hora),
    INDEX idx_origen (origen)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Historial de comandos ejecutados';

-- TABLA: estados_sistema
-- Almacena estados periódicos del sistema completo
CREATE TABLE IF NOT EXISTS estados_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,
    relay_activo BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Estado del relay (ventilador/luz)',
    led_color VARCHAR(20) COMMENT 'Color actual del LED RGB',
    temperatura_actual DECIMAL(5,2) COMMENT 'Última temperatura registrada',
    humedad_actual DECIMAL(5,2) COMMENT 'Última humedad registrada',
    movimiento_activo BOOLEAN DEFAULT FALSE COMMENT 'Estado actual del sensor de movimiento',
    wifi_conectado BOOLEAN DEFAULT FALSE COMMENT 'Estado de conexión WiFi',
    mqtt_conectado BOOLEAN DEFAULT FALSE COMMENT 'Estado de conexión MQTT',
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp del estado',
    INDEX idx_fecha_hora (fecha_hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Snapshots periódicos del estado del sistema';

-- TABLA: alertas_sistema
-- Almacena alertas generadas por el sistema
CREATE TABLE IF NOT EXISTS alertas_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_alerta VARCHAR(50) NOT NULL COMMENT 'Tipo de alerta (movimiento, temperatura, error)',
    severidad ENUM('info', 'advertencia', 'critica') DEFAULT 'info' COMMENT 'Nivel de severidad',
    mensaje TEXT COMMENT 'Descripción de la alerta',
    datos_contexto JSON COMMENT 'Datos adicionales del contexto',
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp de la alerta',
    INDEX idx_tipo_alerta (tipo_alerta),
    INDEX idx_severidad (severidad),
    INDEX idx_fecha_hora (fecha_hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registro de alertas del sistema';

-- TABLA: configuracion_sistema
-- Almacena configuraciones del sistema
CREATE TABLE IF NOT EXISTS configuracion_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(100) NOT NULL UNIQUE COMMENT 'Clave de configuración',
    valor VARCHAR(255) NOT NULL COMMENT 'Valor de configuración',
    descripcion TEXT COMMENT 'Descripción de la configuración',
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_clave (clave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Parámetros de configuración del sistema';

-- INSERTAR CONFIGURACIONES INICIALES
INSERT INTO configuracion_sistema (clave, valor, descripcion) VALUES
('temp_maxima', '28.0', 'Temperatura máxima antes de activar ventilador (°C)'),
('temp_minima', '25.0', 'Temperatura mínima para desactivar ventilador (°C)'),
('intervalo_lectura', '3', 'Intervalo entre lecturas de sensores (segundos)'),
('intervalo_envio_mqtt', '10', 'Cada cuántos ciclos enviar datos por MQTT'),
('cooldown_alerta', '5', 'Tiempo mínimo entre alertas de movimiento (segundos)')
ON DUPLICATE KEY UPDATE valor=VALUES(valor);

-- VISTAS ÚTILES

-- Vista: Últimas 100 lecturas con información completa
CREATE OR REPLACE VIEW vista_lecturas_recientes AS
SELECT 
    id,
    temperatura,
    humedad,
    fecha_hora,
    CASE 
        WHEN temperatura > 28 THEN 'Alta'
        WHEN temperatura < 20 THEN 'Baja'
        ELSE 'Normal'
    END AS clasificacion_temp
FROM lecturas_sensores
ORDER BY fecha_hora DESC
LIMIT 100;

CREATE OR REPLACE VIEW vista_movimientos_por_hora AS
SELECT 
    DATE_FORMAT(fecha_hora, '%
