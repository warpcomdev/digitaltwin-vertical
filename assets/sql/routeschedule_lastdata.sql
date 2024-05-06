CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeschedule_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  hour int,
  zonelist json,
  forwardtrips double precision,
  returntrips double precision,
  forwardstops int,
  location geometry(MultiLineString),
  returnstops int,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeschedule_lastdata_pkey PRIMARY KEY (entityid)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_routeschedule_lastdata_idx_sceneref ON :target_schema.dtwin_routeschedule_lastdata (sceneref, timeinstant);
