-- CREATE VIEW dtwin_routeschedule_vector
-- Vista que extrae las métricas necesarias para calcular
-- el vector de estados que representa a la ciudad.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_routeschedule_vector AS
SELECT
  sourceref AS entityid,
  trend,
  daytype,
  zone,
  ST_Centroid(location) AS location,
  hour,
  0 as minute
FROM :target_schema.dtwin_routeschedule_sim AS t
WHERE sceneref IS NULL OR sceneref = 'NA';