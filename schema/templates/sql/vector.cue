package sql

import (
	"strings"
)

vector: {

	// Parámetros de entrada de la vista:
	input: {
		metrics: [...string] // Diccionario alias => expresión SQL
		hasHour:             bool
		hasMinute:           bool
		multiZone:           bool

		namespace:  string // Prefijo de las tablas
		entityType: string // Tipo de entidad
		tableName:  string | *"\(namespace)_\(strings.ToLower(entityType))_sim"
		viewName:   string | *"\(namespace)_\(strings.ToLower(entityType))_vector"
	}

	template: """
		-- CREATE VIEW {{ .viewName }}
		-- Vista que extrae las métricas necesarias para calcular
		-- el vector de estados que representa a la ciudad.
		-- -------------------------------------------------------------
		DROP VIEW IF EXISTS :target_schema.{{ .viewName }};
		CREATE OR REPLACE VIEW :target_schema.{{ .viewName }} AS
		SELECT
		  {{- range .metrics }}
		  {{.}},
		  {{- end }}
		  sourceref AS entityid,
		  trend,
		  daytype,
		  {{- if !.multiZone }}
		  zone,
		  {{- end }}
		  {{- if .multiZone }}
		  zoneList,
		  {{- end }}
		  ST_Centroid(location) AS location,
		  {{- if .hasHour }}
		  hour,
		  {{- end }}
		  {{- if not .hasHour }}
		  0 as hour,
		  {{- end }}
		  {{- if .hasMinute }}
		  minute
		  {{- end }}
		  {{- if not .hasMinute }}
		  0 as minute
		  {{- end }}
		FROM :target_schema.{{ .tableName }} AS t
		WHERE sceneref IS NULL OR sceneref = 'NA';
		"""

	// Nombres de las relaciones creadas
	relations: [input.viewName]
}
