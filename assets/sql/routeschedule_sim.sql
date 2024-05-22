CREATE OR REPLACE VIEW :target_schema.dtwin_routeschedule_sim AS
  SELECT
    left_table.timeinstant,
    right_table.entityid,
    right_table.entitytype,
    right_table.recvtime,
    right_table.fiwareservicepath,
    right_table.sourceref,
    right_table.sceneref,
    right_table.trend,
    right_table.daytype,
    right_table.hour,
    right_table.name,
    right_table.location,
    right_table.zonelist,
    right_table.forwardstops,
    right_table.returnstops,
    right_table.forwardtrips,
    right_table.returntrips
  FROM
    :target_schema.dtwin_simulation_lastdata left_table
  INNER JOIN
    :target_schema.dtwin_routeschedule_join right_table
  ON left_table.entityId = right_table.sceneRef
    AND left_table.timeinstant = right_table.timeinstant
;
