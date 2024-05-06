CREATE TABLE IF NOT EXISTS :target_schema.dtwin_trend_lastdata (
  timeinstant timestamp with time zone NOT NULL,
  -- Common model attributes
  entityid text,
  entitytype text,
  recvtime timestamp with time zone,
  fiwareservicepath text,
  -- PRIMARY KEYS
  CONSTRAINT dtwin_trend_lastdata_pkey PRIMARY KEY (entityid)
);
