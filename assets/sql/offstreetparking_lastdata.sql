CREATE TABLE IF NOT EXISTS :target_schema.dtwin_offstreetparking_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sourceref text,
  sceneref text,
  trend text,
  daytype text,
  name text,
  hour int,
  zone text,
  capacity double precision,
  occupationpercent double precision,
  location geometry(Point),
  occupation double precision,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_offstreetparking_lastdata_pkey PRIMARY KEY (entityid)
);
