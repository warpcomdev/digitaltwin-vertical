CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeintensity_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  zonelist json,
  forwardtrips double precision,
  returntrips double precision,
  forwardstops int,
  returnstops int,
  location geometry(MultiLineString),
  intensity double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeintensity_lastdata_pkey PRIMARY KEY (entityid)
);
