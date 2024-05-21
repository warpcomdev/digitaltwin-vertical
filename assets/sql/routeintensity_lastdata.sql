CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeintensity_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  name text,
  zonelist json,
  forwardstops integer,
  returnstops integer,
  location geometry(MultiLineString),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeintensity_lastdata_pkey PRIMARY KEY (entityid)
);
