-- CREATE VIEW dtwin_routeintensity_vector
-- Vista que extrae las métricas necesarias para calcular
-- el vector de estados que representa a la ciudad.
-- -------------------------------------------------------------
CREATE OR REPLACE VIEW :target_schema.dtwin_routeintensity_vector AS
SELECT
  intensity,
  sourceref AS entityid,
  trend,
  daytype,
  zone,
  ST_Centroid(location) AS location,
  0 as hour,
  0 as minute
FROM :target_schema.dtwin_routeintensity_lastdata AS t
WHERE sceneref IS NULL OR sceneref = 'NA';