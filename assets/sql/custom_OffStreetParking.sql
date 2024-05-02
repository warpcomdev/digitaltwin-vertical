-- CREATE VIEW dtwin_offstreetparking_daily
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por día. Ignora la hora y minuto.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW %target_schema%.dtwin_offstreetparking_daily AS
SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
  MAX(capacity) AS capacity,
  AVG(occupation) AS occupation,
  SUM(occupation) / SUM(capacity)::double precision AS occupationPercent,
  t.entityid
FROM %target_schema%.dtwin_offstreetparking_lastdata AS t
WHERE t.hour >= 8 AND t.hour <= 22
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.entityid;

-- CREATE VIEW dtwin_offstreetparking_yesterday
-- Vista que reemplaza el timeinstant de la tabla "lastdata"
-- por una fecha calculada que se corresponde al día de ayer.
-- Esto facilita mostrar series temporales genéricas en un
-- widget timeseries de urbo, sin necesidad de tener muestras
-- diarias para todos los días.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW %target_schema%.dtwin_offstreetparking_yesterday AS
SELECT
  timeinstant,
  sourceref,
  sceneref,
  trend,
  daytype,
  name,
  zone,
  capacity,
  occupation,
  occupationPercent,
  entityid,
  date_trunc('day'::text, now()) - '1 day'::interval + make_interval(hours => t.hour) AS generatedinstant
FROM %target_schema%.dtwin_offstreetparking_lastdata AS t;

-- CREATE VIEW dtwin_offstreetparking_yesterday
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
  END) AS "evening_min",
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
  t.hour,
  t.occupationPercent
FROM %target_schema%.dtwin_offstreetparking_lastdata AS t
WHERE t.hour >= 8 AND t.hour <= 22
ORDER BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8, t.occupationPercent DESC) AS ordenadas) AS extremas
WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL

-- CREATE VIEW dtwin_offstreetparking_freq
-- Vista que calcula la frecuencia con la que una métrica
-- está dentro de un umbral.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW %target_schema%.dtwin_offstreetparking_freq AS
SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
  CASE
    WHEN t.occupationPercent < 30 THEN 'tramo_0'
    WHEN t.occupationPercent < 50 THEN 'tramo_1'
    WHEN t.occupationPercent < 70 THEN 'tramo_2'
    WHEN t.occupationPercent < 90 THEN 'tramo_3'
    ELSE 'tramo_4'
  END AS range,
  COUNT(t.hour) AS hours
FROM %target_schema%.dtwin_offstreetparking_lastdata AS t
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8