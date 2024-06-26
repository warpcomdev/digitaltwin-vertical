CREATE TABLE IF NOT EXISTS :target_schema.dtwin_routeschedule (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour integer,
  forwardstops integer,
  returnstops integer,
  forwardtrips double precision,
  returntrips double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_routeschedule_pkey PRIMARY KEY (entityid, timeinstant, sceneref, trend, daytype, hour)
);

-- Indexes coming from dbIndexes in model spec
CREATE INDEX dtwin_routeschedule_idx_scene ON :target_schema.dtwin_routeschedule (timeinstant, sceneRef);
