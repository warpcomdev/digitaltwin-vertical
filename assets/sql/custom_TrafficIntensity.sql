-- CREATE VIEW dtwin_trafficintensity_daily
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por día. Ignora la hora y minuto.
-- -------------------------------------------------------------
DROP VIEW IF EXISTS :target_schema.dtwin_trafficintensity_daily;
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficintensity_daily AS
SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
  SUM(intensity) AS intensity,
  z.name AS zone_name,
  t.entityid
FROM :target_schema.dtwin_trafficintensity_sim AS t
LEFT JOIN :target_schema.dtwin_zone_lastdata z ON t.zone = z.entityid
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.entityid;
-- CREATE VIEW dtwin_trafficintensity_yesterday
-- Vista que reemplaza el timeinstant de la tabla "lastdata"
-- por una fecha calculada que se corresponde al día de ayer.
-- Esto facilita mostrar series temporales genéricas en un
-- widget timeseries de urbo, sin necesidad de tener muestras
-- diarias para todos los días.
-- -------------------------------------------------------------
DROP VIEW IF EXISTS :target_schema.dtwin_trafficintensity_yesterday;
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficintensity_yesterday AS
SELECT
  timeinstant,
  sourceref,
  sceneref,
  trend,
  daytype,
  name,
  zone,
  intensity,
  entityid,
  timezone('CEST'::text, date_trunc('day'::text, timezone('CEST'::text, now())) - '1 day'::interval) + make_interval(hours => t.hour) AS generatedinstant
FROM :target_schema.dtwin_trafficintensity_sim AS t;
-- CREATE VIEW dtwin_trafficintensity_peak
-- Vista que pivota la hora y / o minuto de máximo y mínimo valor de
-- una métrica dada.
-- -------------------------------------------------------------
DROP VIEW IF EXISTS :target_schema.dtwin_trafficintensity_peak;
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficintensity_peak AS
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
    WHEN numeradas.morning = TRUE AND numeradas.is_max IS NULL THEN numeradas.hour
    ELSE NULL
  END) AS "morning_max",
  MAX(CASE
    WHEN numeradas.morning = FALSE AND numeradas.is_max IS NULL THEN numeradas.hour
    ELSE NULL
  END) AS "evening_max",
  MAX(CASE
    WHEN numeradas.morning = TRUE AND numeradas.is_min IS NULL THEN numeradas.hour
    ELSE NULL
  END) AS "morning_min",
  MAX(CASE
    WHEN numeradas.morning = FALSE AND numeradas.is_min IS NULL THEN numeradas.hour
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
    WHEN t.hour < 15 THEN TRUE
    ELSE FALSE
  END AS morning,
  entityid,
  t.hour,
  t.intensity
FROM :target_schema.dtwin_trafficintensity_sim AS t
WHERE t.hour >= 7 AND t.hour < 23
ORDER BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8, t.intensity DESC) AS ordenadas) AS numeradas
WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL
GROUP BY  numeradas.timeinstant, numeradas.sourceref, numeradas.sceneref, numeradas.trend, numeradas.daytype, numeradas.name, numeradas.zone, entityid;