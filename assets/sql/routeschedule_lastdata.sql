CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeschedule_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  name text,
  zonelist json,
  location geometry(MultiLineString),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeschedule_lastdata_pkey PRIMARY KEY (entityid)
);
