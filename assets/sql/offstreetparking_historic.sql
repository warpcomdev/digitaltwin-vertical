CREATE TABLE IF NOT EXISTS :target_schema.dtwin_offstreetparking (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour integer,
  capacity double precision,
  occupationpercent double precision,
  occupation double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_offstreetparking_pkey PRIMARY KEY (entityid, timeinstant, sceneref, trend, daytype, hour)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_offstreetparking_idx_scene ON :target_schema.dtwin_offstreetparking (timeinstant, sceneRef);
