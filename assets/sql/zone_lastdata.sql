CREATE TABLE IF NOT EXISTS :target_schema.dtwin_zone_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  zoneid integer,
  name text,
  label text,
  location geometry(Polygon),
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_zone_lastdata_pkey PRIMARY KEY (entityid)
);
