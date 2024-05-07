CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficintensity (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  intensity double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficintensity_pkey PRIMARY KEY (entityid, timeinstant, sceneref, trend, daytype, hour)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_trafficintensity_idx_scene ON :target_schema.dtwin_trafficintensity (timeinstant, sceneRef);
