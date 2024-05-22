CREATE TABLE IF NOT EXISTS :target_schema.dtwin_simulation_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  sceneref text,
  name text,
  description text,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_simulation_lastdata_pkey PRIMARY KEY (entityid)
);
