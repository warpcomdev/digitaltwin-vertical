package sql

import (
	"strings"
)

peak: {

	// Parámetros de entrada de la vista:
	input: {
		hourFrom:   int    // inicio del intervalo de interés
		hourTo:     int    // fin del intervalo de interés
		morningEnd: int    // hora que marca la separación entre mañana y tarde
		metric:     string // columna que contiene la métrica por la que ordenar
		columns: [...string] // Lista de columnas a agrupar

		namespace:  string // Prefijo de las tablas
		entityType: string // Tipo de entidad
		hasHour:    bool
		hasMinute:  bool
		tableName:  string | *"\(namespace)_\(strings.ToLower(entityType))_lastdata"
		viewName:   string | *"\(namespace)_\(strings.ToLower(entityType))_peak"
	}

	_formula: string | *"numeradas.hour"
	if input.hasMinute {
		_formula: "numeradas.hour || ':' || numeradas.minute"
	}
	sql: """
		-- CREATE VIEW {{ .viewName }}
		-- Vista que pivota la hora y / o minuto de máximo y mínimo valor de
		-- una métrica dada.
		-- -------------------------------------------------------------
		SELECT
		  {{- range .columns }}
		  numeradas.{{.}},
		  {{- end }}
		  MAX(CASE
		    WHEN numeradas.morning = TRUE AND numeradas.is_max IS NULL THEN \(_formula)
		    ELSE NULL
		  END) AS "morning_max",
		  MAX(CASE
		    WHEN numeradas.morning = FALSE AND numeradas.is_max IS NULL THEN \(_formula)
		    ELSE NULL
		  END) AS "evening_max",
		  MAX(CASE
		    WHEN numeradas.morning = TRUE AND numeradas.is_min IS NULL THEN \(_formula)
		    ELSE NULL
		  END) AS "morning_min",
		  MAX(CASE
		    WHEN numeradas.morning = FALSE AND numeradas.is_min IS NULL THEN \(_formula)
		    ELSE NULL
		  END) AS "evening_min",
		FROM (\(_franjas_numeradas)) AS extremas
		WHERE numeradas.is_min IS NULL OR numeradas.is_max IS NULL
		"""

	// Esta query numera las filas de la query anterior,
	// y añade una columna con los valores anterior y posterior en 
	// cada fila de la columna "hour"
	_franjas_numeradas: """
		SELECT *,
		  lead(ordenadas.hour) OVER (
		    PARTITION BY {{ range .columns }} ordenadas.{{.}},{{ end }} ordenadas.morning
		  ) AS is_min,
		  lag(ordenadas.hour) OVER (
		    PARTITION BY {{ range .columns }} ordenadas.{{.}},{{ end }} ordenadas.morning
		  ) AS is_max
		FROM (\(_franjas_ordenadas)) AS ordenadas
		"""

	// Esta query ordena las entradas del periodo seleccionado
	// por valor de la métrica, en orden descendente
	_morningColumn:     len(input.columns) + 1
	_franjas_ordenadas: """
		SELECT
		  {{- range .columns }}
		  t.{{.}},
		  {{- end }}
		  CASE
		    WHEN t.hour <= {{ .morningEnd }} THEN TRUE
		    ELSE FALSE
		  END AS morning,
		  t.hour,
		  {{- if .hasMinute }}
		  t.minute,
		  {{- end }}
		  t.{{ .metric }}
		FROM %target_schema%.{{ .tableName }} AS t
		WHERE t.hour >= {{ .hourFrom }} AND t.hour <= {{ .hourTo }}
		ORDER BY {{ range.columns }} t.{{.}},{{ end }} \(_morningColumn), t.{{ .metric }} DESC
		"""

	// Nombres de las relaciones creadas
	relations: [input.viewName]
}
