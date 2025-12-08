-- ============================================================
-- CONSULTAS ÚTILES PARA EL SISTEMA SMART HOME IOT
-- ============================================================

USE smarthome_iot;

-- ============================================================
-- CONSULTAS DE LECTURAS DE SENSORES
-- ============================================================

-- Últimas 50 lecturas de sensores
SELECT 
    id,
    temperatura,
    humedad,
    fecha_hora
FROM lecturas_sensores
ORDER BY fecha_hora DESC
LIMIT 50;

-- Promedio de temperatura y humedad por hora (últimas 24 horas)
SELECT 
    DATE_FORMAT(fecha_hora, '%Y-%m-%d %H:00') AS hora,
    AVG(temperatura) AS temp_promedio,
    MAX(temperatura) AS temp_maxima,
    MIN(temperatura) AS temp_minima,
    AVG(humedad) AS humedad_promedio
FROM lecturas_sensores
WHERE fecha_hora >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY DATE_FORMAT(fecha_hora, '%Y-%m-%d %H:00')
ORDER BY hora DESC;

-- Lecturas con temperatura fuera del rango normal (< 20°C o > 28°C)
SELECT 
    temperatura,
    humedad,
    fecha_hora,
    CASE 
        WHEN temperatura < 20 THEN 'Baja'
        WHEN temperatura > 28 THEN 'Alta'
    END AS alerta
FROM lecturas_sensores
WHERE temperatura < 20 OR temperatura > 28
ORDER BY fecha_hora DESC;

-- ============================================================
-- CONSULTAS DE EVENTOS DE MOVIMIENTO
-- ============================================================

-- Todos los eventos de movimiento del día
SELECT 
    id,
    temperatura_momento,
    humedad_momento,
    fecha_hora
FROM eventos_movimiento
WHERE DATE(fecha_hora) = CURDATE()
ORDER BY fecha_hora DESC;

-- Número de eventos de movimiento por día (última semana)
SELECT 
    DATE(fecha_hora) AS fecha,
    COUNT(*) AS total_eventos
FROM eventos_movimiento
WHERE fecha_hora >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(fecha_hora)
ORDER BY fecha DESC;

-- Detección de patrones: horas con más movimiento
SELECT 
    HOUR(fecha_hora) AS hora_del_dia,
    COUNT(*) AS total_detecciones
FROM eventos_movimiento
WHERE detectado = TRUE
GROUP BY HOUR(fecha_hora)
ORDER BY total_detecciones DESC;

-- ============================================================
-- CONSULTAS DE COMANDOS Y CONTROL
-- ============================================================

-- Últimos 100 comandos ejecutados
SELECT 
    dispositivo,
    accion,
    origen,
    fecha_hora
FROM comandos_control
ORDER BY fecha_hora DESC
LIMIT 100;

-- Comandos agrupados por dispositivo (hoy)
SELECT 
    dispositivo,
    COUNT(*) AS total_comandos,
    GROUP_CONCAT(DISTINCT accion) AS acciones
FROM comandos_control
WHERE DATE(fecha_hora) = CURDATE()
GROUP BY dispositivo;

-- Activaciones del relay (ventilador/luz) en las últimas 24 horas
SELECT 
    accion,
    origen,
    fecha_hora
FROM comandos_control
WHERE dispositivo = 'relay'
  AND fecha_hora >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY fecha_hora DESC;

-- ============================================================
-- CONSULTAS DE ESTADOS DEL SISTEMA
-- ============================================================

-- Último estado registrado del sistema
SELECT 
    relay_activo,
    led_color,
    temperatura_actual,
    humedad_actual,
    movimiento_activo,
    wifi_conectado,
    mqtt_conectado,
    fecha_hora
FROM estados_sistema
ORDER BY fecha_hora DESC
LIMIT 1;

-- Historial de estados del relay (ON/OFF) hoy
SELECT 
    relay_activo,
    temperatura_actual,
    fecha_hora
FROM estados_sistema
WHERE DATE(fecha_hora) = CURDATE()
ORDER BY fecha_hora DESC;

-- ============================================================
-- CONSULTAS DE ALERTAS
-- ============================================================

-- Últimas 50 alertas del sistema
SELECT 
    tipo_alerta,
    severidad,
    mensaje,
    fecha_hora
FROM alertas_sistema
ORDER BY fecha_hora DESC
LIMIT 50;

-- Alertas críticas no resueltas
SELECT 
    tipo_alerta,
    mensaje,
    datos_contexto,
    fecha_hora
FROM alertas_sistema
WHERE severidad = 'critica'
ORDER BY fecha_hora DESC;

-- Conteo de alertas por tipo (última semana)
SELECT 
    tipo_alerta,
    COUNT(*) AS total
FROM alertas_sistema
WHERE fecha_hora >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY tipo_alerta
ORDER BY total DESC;

-- ============================================================
-- CONSULTAS ANALÍTICAS
-- ============================================================

-- Dashboard: Resumen general del día
SELECT 
    (SELECT COUNT(*) FROM lecturas_sensores WHERE DATE(fecha_hora) = CURDATE()) AS total_lecturas,
    (SELECT AVG(temperatura) FROM lecturas_sensores WHERE DATE(fecha_hora) = CURDATE()) AS temp_promedio,
    (SELECT COUNT(*) FROM eventos_movimiento WHERE DATE(fecha_hora) = CURDATE()) AS total_movimientos,
    (SELECT COUNT(*) FROM comandos_control WHERE DATE(fecha_hora) = CURDATE()) AS total_comandos,
    (SELECT COUNT(*) FROM alertas_sistema WHERE DATE(fecha_hora) = CURDATE()) AS total_alertas;

-- Correlación: Temperatura vs Activaciones de Relay
SELECT 
    ROUND(ls.temperatura, 0) AS rango_temperatura,
    COUNT(*) AS veces_activado
FROM comandos_control cc
JOIN lecturas_sensores ls ON DATE(cc.fecha_hora) = DATE(ls.fecha_hora)
WHERE cc.dispositivo = 'relay' 
  AND cc.accion = 'encender'
GROUP BY ROUND(ls.temperatura, 0)
ORDER BY rango_temperatura;

-- Tiempo promedio entre eventos de movimiento
SELECT 
    AVG(TIMESTAMPDIFF(SECOND, 
        LAG(fecha_hora) OVER (ORDER BY fecha_hora),
        fecha_hora
    )) AS segundos_promedio_entre_eventos
FROM eventos_movimiento
WHERE DATE(fecha_hora) = CURDATE();

-- ============================================================
-- LIMPIEZA Y MANTENIMIENTO
-- ============================================================

-- Eliminar lecturas anteriores a 30 días (ejecutar periódicamente)
-- DELETE FROM lecturas_sensores WHERE fecha_hora < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Eliminar eventos de movimiento anteriores a 30 días
-- DELETE FROM eventos_movimiento WHERE fecha_hora < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Eliminar comandos anteriores a 30 días
-- DELETE FROM comandos_control WHERE fecha_hora < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- ============================================================
-- CONSULTAS DE EXPORTACIÓN
-- ============================================================

-- Exportar datos del día para análisis (formato CSV)
SELECT 
    DATE_FORMAT(fecha_hora, '%Y-%m-%d %H:%i:%s') AS timestamp,
    temperatura,
    humedad
FROM lecturas_sensores
WHERE
