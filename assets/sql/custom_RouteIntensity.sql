-- CREATE VIEW dtwin_routeintensity_daily
-- Vista que agrega todos los resultados de una tabla de gemelo,
-- por día. Ignora la hora y minuto.
-- -------------------------------------------------------------
DROP VIEW IF EXISTS :target_schema.dtwin_routeintensity_daily;
CREATE OR REPLACE VIEW :target_schema.dtwin_routeintensity_daily AS
SELECT
  t.timeinstant,
  t.sourceref,
  t.sceneref,
  t.trend,
  t.daytype,
  t.name,
  t.zone,
  sum(t.intensity) / sum(t.forwardtrips * t.forwardstops + t.returntrips * t.returnstops) AS intensity_per_stop,
  sum(t.intensity) / sum(t.forwardtrips + t.returntrips)::double precision AS intensity_per_trip,
  t.entityid
FROM :target_schema.dtwin_routeintensity_sim AS t
GROUP BY  t.timeinstant, t.sourceref, t.sceneref, t.trend, t.daytype, t.name, t.zone, t.entityid;