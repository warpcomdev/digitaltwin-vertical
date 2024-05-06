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

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_trafficintensity_lastdata_idx_sceneref ON :target_schema.dtwin_trafficintensity_lastdata (sceneref, timeinstant);
