CREATE OR REPLACE VIEW :target_schema.dtwin_trafficcongestion_join AS
  SELECT
    left_table.entityid,
    left_table.entityType,
    left_table.fiwareservicepath,
    left_table.recvtime,
    left_table.timeinstant,
    left_table.sourceref,
    left_table.sceneref,
    left_table.trend,
    left_table.daytype,
    left_table.hour,
    left_table.minute,
    left_table.congestion,
    right_table.name,
    right_table.location,
    right_table.zone
  FROM
    :target_schema.dtwin_trafficcongestion left_table
  INNER JOIN
    :target_schema.dtwin_trafficcongestion_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
