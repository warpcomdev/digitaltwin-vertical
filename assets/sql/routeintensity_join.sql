CREATE OR REPLACE VIEW :target_schema.dtwin_routeintensity_join AS
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
    left_table.zonelist,
    left_table.forwardtrips,
    left_table.returntrips,
    left_table.forwardstops,
    left_table.returnstops,
    left_table.intensity,
    right_table.name,
    right_table.location
  FROM
    :target_schema.dtwin_routeintensity left_table
  INNER JOIN
    :target_schema.dtwin_routeintensity_lastdata right_table
  ON left_table.entityid = right_table.entityid
;
