CREATE OR REPLACE VIEW :target_schema.dtwin_routeintensity_sim AS
  SELECT
    left_table.TimeInstant,
    right_table.sourceref,
    right_table.sceneref,
    right_table.trend,
    right_table.daytype,
    right_table.name,
    right_table.location,
    right_table.zonelist,
    right_table.forwardtrips,
    right_table.returntrips,
    right_table.forwardstops,
    right_table.returnstops,
    right_table.intensity
  FROM
    :target_schema.dtwin_simulation_lastdata left_table
  INNER JOIN
    :target_schema.dtwin_routeintensity_lastdata right_table
  ON left_table.entityId = right_table.sceneRef
    AND left_table.TimeInstant = right_table.TimeInstant
;
