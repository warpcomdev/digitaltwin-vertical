CREATE TABLE IF NOT EXISTS :target_schema.dtwin_offstreetparking (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  zone text,
  capacity double precision,
  occupationpercent double precision,
  occupation double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_offstreetparking_pkey PRIMARY KEY (timeinstant, entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeintensity (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  zonelist json,
  forwardtrips double precision,
  returntrips double precision,
  forwardstops int,
  returnstops int,
  intensity double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeintensity_pkey PRIMARY KEY (timeinstant, entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeschedule (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  zonelist json,
  forwardtrips double precision,
  returntrips double precision,
  forwardstops int,
  returnstops int,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeschedule_pkey PRIMARY KEY (timeinstant, entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficcongestion (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  minute int,
  zone text,
  congestion double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficcongestion_pkey PRIMARY KEY (timeinstant, entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficintensity (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  zone text,
  intensity double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficintensity_pkey PRIMARY KEY (timeinstant, entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_daytype_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_daytype_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_offstreetparking_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  hour int,
  zone text,
  capacity double precision,
  occupationpercent double precision,
  location geometry(Point),
  occupation double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_offstreetparking_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeintensity_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  zonelist json,
  forwardtrips double precision,
  returntrips double precision,
  forwardstops int,
  returnstops int,
  location geometry(MultiLine),
  intensity double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeintensity_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeschedule_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  hour int,
  zonelist json,
  forwardtrips double precision,
  returntrips double precision,
  forwardstops int,
  location geometry(MultiLine),
  returnstops int,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeschedule_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficcongestion_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  hour int,
  minute int,
  zone text,
  congestion double precision,
  location geometry(Point),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficcongestion_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficintensity_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  hour int,
  zone text,
  intensity double precision,
  location geometry(Point),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficintensity_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE TABLE IF NOT EXISTS :target_schema.dtwin_zone_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  zoneid int,
  name text,
  label text,
  location geometry(Polygon),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_zone_lastdata_pkey PRIMARY KEY (entityid)
);
CREATE OR REPLACE VIEW :target_schema.dtwin_offstreetparking_join AS
  SELECT
    left_table.entityid,
    left_table.entityType,
    left_table.fiwareservicepath,
    left_table.recvtime,
    left_table.timeinstant,
    left_table.sourceref,
    left_table.sceneref,
    left_table.trend,
    left_table.daytype,
    left_table.hour,
    left_table.zone,
    left_table.capacity,
    left_table.occupationpercent,
    left_table.occupation,
    right_table.name,
    right_table.location
  FROM
    :target_schema.dtwin_offstreetparking left_table
  INNER JOIN
    :target_schema.dtwin_offstreetparking_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
CREATE OR REPLACE VIEW :target_schema.dtwin_routeintensity_join AS
  SELECT
    left_table.entityid,
    left_table.entityType,
    left_table.fiwareservicepath,
    left_table.recvtime,
    left_table.timeinstant,
    left_table.sourceref,
    left_table.sceneref,
    left_table.trend,
    left_table.daytype,
    left_table.zonelist,
    left_table.forwardtrips,
    left_table.returntrips,
    left_table.forwardstops,
    left_table.returnstops,
    left_table.intensity,
    right_table.name,
    right_table.location
  FROM
    :target_schema.dtwin_routeintensity left_table
  INNER JOIN
    :target_schema.dtwin_routeintensity_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
CREATE OR REPLACE VIEW :target_schema.dtwin_routeschedule_join AS
  SELECT
    left_table.entityid,
    left_table.entityType,
    left_table.fiwareservicepath,
    left_table.recvtime,
    left_table.timeinstant,
    left_table.sourceref,
    left_table.sceneref,
    left_table.trend,
    left_table.daytype,
    left_table.hour,
    left_table.zonelist,
    left_table.forwardtrips,
    left_table.returntrips,
    left_table.forwardstops,
    left_table.returnstops,
    right_table.name,
    right_table.location
  FROM
    :target_schema.dtwin_routeschedule left_table
  INNER JOIN
    :target_schema.dtwin_routeschedule_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficcongestion_join AS
  SELECT
    left_table.entityid,
    left_table.entityType,
    left_table.fiwareservicepath,
    left_table.recvtime,
    left_table.timeinstant,
    left_table.sourceref,
    left_table.sceneref,
    left_table.trend,
    left_table.daytype,
    left_table.hour,
    left_table.minute,
    left_table.zone,
    left_table.congestion,
    right_table.name,
    right_table.location
  FROM
    :target_schema.dtwin_trafficcongestion left_table
  INNER JOIN
    :target_schema.dtwin_trafficcongestion_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
CREATE OR REPLACE VIEW :target_schema.dtwin_trafficintensity_join AS
  SELECT
    left_table.entityid,
    left_table.entityType,
    left_table.fiwareservicepath,
    left_table.recvtime,
    left_table.timeinstant,
    left_table.sourceref,
    left_table.sceneref,
    left_table.trend,
    left_table.daytype,
    left_table.hour,
    left_table.zone,
    left_table.intensity,
    right_table.name,
    right_table.location
  FROM
    :target_schema.dtwin_trafficintensity left_table
  INNER JOIN
    :target_schema.dtwin_trafficintensity_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
-- CREATE VIEW dtwin_offstreetparking_daily
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por día. Ignora la hora y minuto.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_offstreetparking_daily AS
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
FROM :target_schema.dtwin_offstreetparking_lastdata AS t
WHERE t.hour >= 8 AND t.hour <= 22
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.entityid;

-- CREATE VIEW dtwin_offstreetparking_yesterday
-- Vista que reemplaza el timeinstant de la tabla "lastdata"
-- por una fecha calculada que se corresponde al día de ayer.
-- Esto facilita mostrar series temporales genéricas en un
-- widget timeseries de urbo, sin necesidad de tener muestras
-- diarias para todos los días.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_offstreetparking_yesterday AS
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
FROM :target_schema.dtwin_offstreetparking_lastdata AS t;

-- CREATE VIEW dtwin_offstreetparking_peak
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
FROM :target_schema.dtwin_offstreetparking_lastdata AS t
WHERE t.hour >= 8 AND t.hour <= 22
ORDER BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8, t.occupationPercent DESC) AS ordenadas) AS extremas
WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL

-- CREATE VIEW dtwin_offstreetparking_freq
-- Vista que calcula la frecuencia con la que una métrica
-- está dentro de un umbral.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_offstreetparking_freq AS
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
FROM :target_schema.dtwin_offstreetparking_lastdata AS t
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8-- CREATE VIEW dtwin_trafficcongestion_daily
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
  date_trunc('day'::text, now()) - '1 day'::interval  + make_interval(hours => t.hour, minutes => t.minute) AS generatedinstant
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
  t.minute,
  t.congestion
FROM :target_schema.dtwin_trafficcongestion_lastdata AS t
WHERE t.hour >= 7 AND t.hour <= 22
ORDER BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8, t.congestion DESC) AS ordenadas) AS extremas
WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL-- CREATE VIEW dtwin_trafficintensity_daily
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por día. Ignora la hora y minuto.
-- -------------------------------------------------------------
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
  t.entityid
FROM :target_schema.dtwin_trafficintensity_lastdata AS t
WHERE t.hour >= 7 AND t.hour <= 22
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.entityid;

-- CREATE VIEW dtwin_trafficintensity_yesterday
-- Vista que reemplaza el timeinstant de la tabla "lastdata"
-- por una fecha calculada que se corresponde al día de ayer.
-- Esto facilita mostrar series temporales genéricas en un
-- widget timeseries de urbo, sin necesidad de tener muestras
-- diarias para todos los días.
-- -------------------------------------------------------------
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
  date_trunc('day'::text, now()) - '1 day'::interval + make_interval(hours => t.hour) AS generatedinstant
FROM :target_schema.dtwin_trafficintensity_lastdata AS t;

-- CREATE VIEW dtwin_trafficintensity_peak
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
  t.intensity
FROM :target_schema.dtwin_trafficintensity_lastdata AS t
WHERE t.hour >= 7 AND t.hour <= 22
ORDER BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, 8, t.intensity DESC) AS ordenadas) AS extremas
WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL