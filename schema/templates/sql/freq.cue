package sql

import (
	"strings"
)

freq: {

	// Parámetros de entrada de la vista:
	input: {
		metric: string // columna con la métrica a calcular
		other:  string // etiqueta para el último rango
		columns: [...string] // Lista de columnas a agrupar
		ranges: [string]: number // Etiquetas y umbrales de los rangos

		namespace:  string // Prefijo de las tablas
		entityType: string // Tipo de entidad
		hasHour:    bool
		hasMinute:  bool
		tableName:  string | *"\(namespace)_\(strings.ToLower(entityType))_sim"
		viewName:   string | *"\(namespace)_\(strings.ToLower(entityType))_freq"
	}

	_rangeColumn: len(input.columns) + 1
	sql:          """
		-- CREATE VIEW {{ .viewName }}
		-- Vista que calcula la frecuencia con la que una métrica
		-- está dentro de un umbral.
		-- -------------------------------------------------------------
		CREATE OR REPLACE VIEW :target_schema.{{ .viewName }} AS
		SELECT
		  {{- range .columns }}
		  t.{{.}},
		  {{- end }}
		  CASE
		    {{- $metric := .metric }}
		    {{- range $label, $threshold := .ranges }}
		    WHEN t.{{ $metric }} < {{ $threshold }} THEN '{{ $label }}'
			{{- end }}
		    ELSE '{{ .other }}'
		  END AS range,
		  COUNT(t.hour) AS hours
		FROM :target_schema.{{ .tableName }} AS t
		GROUP BY {{ range .columns }} t.{{.}},{{ end }} \(_rangeColumn);
		"""

	// Nombres de las relaciones creadas
	relations: [input.viewName]
}
