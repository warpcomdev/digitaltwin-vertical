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
