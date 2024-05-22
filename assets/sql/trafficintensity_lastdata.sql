CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trafficintensity_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  name text,
  zone text,
  location geometry(Point),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trafficintensity_lastdata_pkey PRIMARY KEY (entityid)
);
