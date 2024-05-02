CREATE TABLE IF NOT EXISTS :target_schema.dtwin_offstreetparking (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  hour int,
  zone text,
  capacity double precision,
  occupationpercent double precision,
  occupation double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_offstreetparking_pkey PRIMARY KEY (timeinstant, entityid)
);
