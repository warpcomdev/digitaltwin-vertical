CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeintensity (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
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
  CONSTRAINT dtwin_routeintensity_pkey PRIMARY KEY (entityid, timeinstant, sceneref, trend, daytype)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_routeintensity_idx_scene ON :target_schema.dtwin_routeintensity (timeinstant, sceneRef);
