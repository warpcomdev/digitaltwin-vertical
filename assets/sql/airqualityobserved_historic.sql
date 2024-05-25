CREATE TABLE IF NOT EXISTS :target_schema.dtwin_airqualityobserved (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  no2 double precision,
  pm25 double precision,
  pm10 double precision,
  o3 double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_airqualityobserved_pkey PRIMARY KEY (entityid, timeinstant, sceneref, trend, daytype)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_airqualityobserved_idx_scene ON :target_schema.dtwin_airqualityobserved (timeinstant, sceneRef);
