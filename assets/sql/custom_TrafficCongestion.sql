-- CREATE VIEW dtwin_trafficcongestion_vector
-- Vista que extrae las métricas necesarias para calcular
-- el vector de estados que representa a la ciudad.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficcongestion_vector AS
SELECT
  congestion,
  sourceref AS entityid,
  trend,
  daytype,
  zone,
  ST_Centroid(location) AS location,
  hour,
  minute
FROM :target_schema.dtwin_trafficcongestion_lastdata AS t
WHERE sceneref IS NULL OR sceneref = 'NA';

-- CREATE VIEW dtwin_trafficcongestion_daily
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por día. Ignora la hora y minuto.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficcongestion_daily AS
SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
  AVG(congestion) AS congestion,
  t.entityid
FROM :target_schema.dtwin_trafficcongestion_lastdata AS t
WHERE t.hour >= 7 AND t.hour <= 22
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.entityid;

-- CREATE VIEW dtwin_trafficcongestion_hourly
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por hora. Ignora el minuto.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficcongestion_hourly AS
SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
t.hour,
  AVG(congestion) AS congestion,
  t.entityid
FROM :target_schema.dtwin_trafficcongestion_lastdata AS t
WHERE t.hour >= 7 AND t.hour <= 22
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.hour, t.entityid;

-- CREATE VIEW dtwin_trafficcongestion_yesterday
-- Vista que reemplaza el timeinstant de la tabla "lastdata"
-- por una fecha calculada que se corresponde al día de ayer.
-- Esto facilita mostrar series temporales genéricas en un
-- widget timeseries de urbo, sin necesidad de tener muestras
-- diarias para todos los días.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficcongestion_yesterday AS
SELECT
  timeinstant,
  sourceref,
  sceneref,
  trend,
  daytype,
  name,
  zone,
  congestion,
  entityid,
  date_trunc('day'::text, now()) - '1 day'::interval  + make_interval(hours => t.hour, mins => t.minute) AS generatedinstant
FROM :target_schema.dtwin_trafficcongestion_lastdata AS t;

-- CREATE VIEW dtwin_trafficcongestion_peak
-- Vista que pivota la hora y / o minuto de máximo y mínimo valor de
-- una métrica dada.
-- -------------------------------------------------------------
SELECT
  numeradas.timeinstant,
  numeradas.sourceref,
  numeradas.sceneref,
  numeradas.trend,
  numeradas.daytype,
  numeradas.name,
  numeradas.zone,
  entityid,
  MAX(CASE
    WHEN numeradas.morning = TRUE AND numeradas.is_max IS NULL THEN numeradas.hour || ':' || numeradas.minute
    ELSE NULL
  END) AS "morning_max",
  MAX(CASE
    WHEN numeradas.morning = FALSE AND numeradas.is_max IS NULL THEN numeradas.hour || ':' || numeradas.minute
    ELSE NULL
  END) AS "evening_max",
  MAX(CASE
    WHEN numeradas.morning = TRUE AND numeradas.is_min IS NULL THEN numeradas.hour || ':' || numeradas.minute
    ELSE NULL
  END) AS "morning_min",
  MAX(CASE
    WHEN numeradas.morning = FALSE AND numeradas.is_min IS NULL THEN numeradas.hour || ':' || numeradas.minute
    ELSE NULL
  END) AS "evening_min"
FROM (SELECT *,
  lead(ordenadas.hour) OVER (
    PARTITION BY  ordenadas.timeinstant, ordenadas.sourceref, ordenadas.sceneref, ordenadas.trend, ordenadas.daytype, ordenadas.name, ordenadas.zone, ordenadas.morning
  ) AS is_min,
  lag(ordenadas.hour) OVER (
    PARTITION BY  ordenadas.timeinstant, ordenadas.sourceref, ordenadas.sceneref, ordenadas.trend, ordenadas.daytype, ordenadas.name, ordenadas.zone, ordenadas.morning
  ) AS is_max
FROM (SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
  CASE
    WHEN t.hour <= 14 THEN TRUE
    ELSE FALSE
  END AS morning,
  entityid,
  t.hour,
  t.minute,
  t.congestion
FROM :target_schema.dtwin_trafficcongestion_lastdata AS t
WHERE t.hour >= 7 AND t.hour <= 22
ORDER BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8, t.congestion DESC) AS ordenadas) AS numeradas
WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL
GROUP BY  numeradas.timeinstant, numeradas.sourceref, numeradas.sceneref, numeradas.trend, numeradas.daytype, numeradas.name, numeradas.zone, entityid;