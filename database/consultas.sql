-- Consultas MySQL para Smart Home IoT

-- Ver ultimas 10 lecturas
SELECT * FROM lecturas_sensores 
ORDER BY timestamp DESC LIMIT 10;

-- Ver todas las lecturas de hoy
SELECT * FROM lecturas_sensores 
WHERE DATE(timestamp) = CURDATE()
ORDER BY timestamp DESC;

-- Estadisticas generales
SELECT 
    COUNT(*) as total_lecturas,
    AVG(temperatura) as temp_promedio,
    MAX(temperatura) as temp_maxima,
    MIN(temperatura) as temp_minima,
    AVG(humedad) as hum_promedio
FROM lecturas_sensores;

-- Ver eventos/alertas
SELECT * FROM eventos 
ORDER BY timestamp DESC LIMIT 10;

-- Ver comandos ejecutados
SELECT * FROM comandos 
ORDER BY timestamp DESC LIMIT 10;

-- Lecturas con temperatura alta
SELECT * FROM lecturas_sensores 
WHERE temperatura > 26
ORDER BY timestamp DESC;

-- Contar detecciones de movimiento
SELECT COUNT(*) as total_movimientos
FROM lecturas_sensores 
WHERE movimiento = 1;
