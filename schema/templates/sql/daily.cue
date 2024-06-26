package sql

import (
	"strings"
)

daily: {

	// Parámetros de entrada de la vista:
	input: {
		columns: [...string] // Lista de columnas a agrupar
		aggregations: [string]: string // Diccionario alias => expresión SQL
		where:    string | *"" // "Where" clause to apply
		withZone: bool | *false

		namespace:  string // Prefijo de las tablas
		entityType: string // Tipo de entidad
		tableName:  string | *"\(namespace)_\(strings.ToLower(entityType))_sim"
		viewName:   string | *"\(namespace)_\(strings.ToLower(entityType))_daily"
	}

	template: """
		-- CREATE VIEW {{ .viewName }}
		-- Vista que agrega todos los resultados de una tabla de gemelo,
		-- por día. Ignora la hora y minuto.
		-- -------------------------------------------------------------
		DROP VIEW IF EXISTS :target_schema.{{ .viewName }};
		CREATE OR REPLACE VIEW :target_schema.{{ .viewName }} AS
		SELECT
		{{- range .columns }}
		  t.{{.}},
		{{- end }}
		{{- range $colname, $agg := .aggregations }}
		  {{ $agg }} AS {{ $colname }},
		{{- end }}
		{{- if .withZone }}
		  z.name AS zone_name,
		{{- end }}
		  t.entityid
		FROM :target_schema.{{ .tableName }} AS t
		{{- if .withZone }}
		LEFT JOIN :target_schema.dtwin_zone_lastdata z ON t.zone = z.entityid
		{{- end }}
		{{- if .filter }}
		WHERE {{ .filter }}
		{{- end }}
		GROUP BY {{ range .columns }} t.{{.}},{{end}} t.entityid;
		"""

	// Nombres de las relaciones creadas
	relations: [input.viewName]
}
