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
  location geometry(LineString),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficcongestion_lastdata_pkey PRIMARY KEY (entityid)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_trafficcongestion_lastdata_idx_sceneref ON :target_schema.dtwin_trafficcongestion_lastdata (sceneref, timeinstant);
