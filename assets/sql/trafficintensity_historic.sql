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
