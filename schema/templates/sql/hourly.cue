package sql

import (
	"strings"
	"text/template"
)

// Vista que agrega todos los resultados de una tabla de gemelo,
// por hora. Ignora el minuto.
hourly: {

	// Parámetros de entrada de la vista:
	input: {
		hourFrom: int // Inicio del periodo de agregación
		hourTo:   int // Fin del periodo de agregación
		columns: [...string] // Lista de columnas a agrupar
		aggregations: [string]: string // Diccionario alias => expresión SQL

		namespace:  string // Prefijo de las tablas
		entityType: string // Tipo de entidad
		tableName:  string | *"\(namespace)_\(strings.ToLower(entityType))_lastdata"
		viewName:   string | *"\(namespace)_\(strings.ToLower(entityType))_hourly"
	}

	_sql: """
		CREATE OR REPLACE VIEW %target_schema%.{{ .viewName }} AS
		SELECT
		{{- range .columns }}
		  t.{{.}},
		{{- end }}
		t.hour,
		{{- range $colname, $agg := .aggregations }}
		  {{ $agg }} AS {{ $colname }},
		{{- end }}
		  t.entityid
		FROM %target_schema%.{{ .tableName }} AS t
		WHERE t.hour >= {{ .hourFrom }} AND t.hour <= {{ .hourTo }}
		GROUP BY {{ range .columns }} t.{{.}},{{end}} t.hour, t.entityid;
		"""

	// Texto del SQL, una vez reemplazados los valores
	output: template.Execute(_sql, input)

	// Nombres de las relaciones creadas
	relations: [input.viewName]
}
