CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficcongestion (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  minute int,
  congestion double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficcongestion_pkey PRIMARY KEY (entityid, timeinstant, sceneref, trend, daytype, hour, minute)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_trafficcongestion_idx_scene ON :target_schema.dtwin_trafficcongestion (timeinstant, sceneRef);
