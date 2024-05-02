package sql

import (
	"strings"
)

yesterday: {

	// Parámetros de entrada de la vista:
	input: {
		columns: [...string] // Lista de columnas a agrupar

		namespace:  string // Prefijo de las tablas
		entityType: string // Tipo de entidad
		hasHour:    bool
		hasMinute:  bool
		tableName:  string | *"\(namespace)_\(strings.ToLower(entityType))_lastdata"
		viewName:   string | *"\(namespace)_\(strings.ToLower(entityType))_yesterday"
		interval:   string | *""
		if hasMinute {
			interval: " + make_interval(hours => t.hour, mins => t.minute)"
		}
		if !hasMinute && hasHour {
			interval: "+ make_interval(hours => t.hour)"
		}
	}

	sql: """
		-- CREATE VIEW {{ .viewName }}
		-- Vista que reemplaza el timeinstant de la tabla "lastdata"
		-- por una fecha calculada que se corresponde al día de ayer.
		-- Esto facilita mostrar series temporales genéricas en un
		-- widget timeseries de urbo, sin necesidad de tener muestras
		-- diarias para todos los días.
		-- -------------------------------------------------------------
		CREATE OR REPLACE VIEW :target_schema.{{ .viewName }} AS
		SELECT
		{{- range .columns }}
		  {{.}},
		{{- end }}
		{{- range $colname, $agg := .aggregations }}
		  {{ $agg }} AS {{ $colname }},
		{{- end }}
		  entityid,
		  date_trunc('day'::text, now()) - '1 day'::interval {{ .interval }} AS generatedinstant
		FROM :target_schema.{{ .tableName }} AS t;
		"""

	// Nombres de las relaciones creadas
	relations: [input.viewName]
}
