package templates

import (
	"list"
	"strings"

	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates/sql"
)

#Twin: self={

	#entityType:   string
	#hasHour:      bool | *true
	#hasMinute:    bool | *false
	#multiZone:    bool | *false
	#geometryType: *"Point" | "LineString" | "MultiLineString" | "Polygon" | "MultiPolygon"
	#namespace:    "dtwin"

	description: string
	namespace:   #namespace
	exampleId:   string

	model: [string]: {
		types.#ModelAttribute
		#metric: bool | *false
	}

	model: {

		TimeInstant: {
			types.#DateTime
			description: "Fecha / Hora del cálculo de vista identidad o simulación"
			flows: ["historic", "lastdata"]
		}

		sourceRef: {
			types.#Text
			description: """
				ID de entidad original.
				Reemplaza al entityId, ya que esta entidad es *singleton*
				y su ID en base de datos se ve sobrescrito por una
				composición de los campos únicos.

				En el caso de las entidades tipo `\(#entityType)`, la columna entityid
				de la base de datos contendrá una concatenación de los siguientes
				atributos, separados por `_`:
				
				`\(strings.Join(#aspects.singleton.attrs, "`, `"))`
				"""
			flows: ["historic", "lastdata"]
			if !#hasMinute && !#hasHour {
				example: "NA_Entity1_Verano_Sabado"
			}
			if !#hasMinute && #hasHour {
				example: "NA_Entity1_Verano_Sabado_21"
			}
			if #hasMinute {
				example: "NA_Entity1_Verano_Sabado_21_30"
			}
		}

		sceneRef: {
			types.#Text
			description: """
				ID del escenario de simulación.
				Identifica la simulación realizada. El valor "NA"
				indica que se trata de una vista identidad.
				"""
			flows: ["historic", "lastdata"]
		}

		trend: {
			types.#Text
			description: "Estacionalidad o tendencia para la que se ha calculado el escenario"
			flows: ["historic", "lastdata"]
			#range: ["Verano", "Fallas", "Otros"]
		}

		dayType: {
			types.#Text
			description: "Tipo de día al que corresponde la medida"
			flows: ["historic", "lastdata"]
			#range: ["L-J", "Viernes", "Sábado", "Domingo"]
		}

		if #hasHour {
			hour: {
				types.#Integer
				description: "Hora del día a la que corresponde la medida"
				flows: ["historic", "lastdata"]
				range:   "0-23"
				example: 15
			}
		}

		if #hasMinute {
			minute: {
				types.#Integer
				description: "Intervalo de 10 minutos al que corresponde la medida"
				flows: ["historic", "lastdata"]
				range:   "0-50"
				example: 20
			}
		}

		name: {
			types.#Text
			description: "Nombre descriptivo de la entidad"
			flows: ["lastdata"]
		}

		location: {
			types.#Geometry[#geometryType]
			description: "Ubicación de la entidad"
			flows: ["lastdata"]
		}

		if !#multiZone {
			zone: {
				types.#Text
				description: "Identificador de la zona o distrito a la que pertenece la entidad"
				example:     "Distrito 1"
				flows: ["historic", "lastdata"]
			}
		}

		if #multiZone {
			zoneList: {
				types.#Array
				description: "Lista de identificadores de la zona o distrito a la que pertenece la entidad"
				example: ["Distrito 1", "Distrito 4"]
				flows: ["historic", "lastdata"]
			}
		}
	}

	#aspects: singleton: {
		{
			class: "ASPECT_SINGLETON"
			// El orden de los atributos es importante
			attrs: [...string]
			if !#hasHour && !#hasMinute {
				attrs: ["sceneRef", "sourceRef", "trend", "dayType"]
			}
			if #hasHour && !#hasMinute {
				attrs: ["sceneRef", "sourceRef", "trend", "dayType", "hour"]
			}
			if #hasMinute {
				attrs: ["sceneRef", "sourceRef", "trend", "dayType", "hour", "minute"]
			}
		}
	}

	aspects: [for _, aspect in #aspects {aspect}]

	flows: {
		historic: {
			class:    "FLOW_HISTORIC"
			endpoint: "HISTORIC"
		}
		lastdata: {
			class:    "FLOW_LASTDATA"
			endpoint: "LASTDATA"
			condition: {
				attrs: ["TimeInstant"] + #aspects.singleton.attrs
				// No quiero que me borre las filas de la tabla,
				// cuando se borren las entidades. Me aseguro de
				// excluir el alterationType onDelete.
				alterationTypes: [
					"entityUpdate",
					"entityCreate",
				]
			}
		}
		join: {
			class:      "FLOW_JOIN_VIEW"
			#tableName: strings.ToLower(#entityType)
			leftModel: {
				name:            #tableName
				entityNamespace: #namespace
				attrs: [
					"entityid", "entityType", "fiwareservicepath", "recvtime",
				] + [for label, m in self.model if list.Contains(m.flows, "historic") {
					strings.ToLower(label)
				}]
				attrJoinOn: ["entityid"]
			}
			rightModel: [{
				name:            "\(#tableName)_lastdata"
				entityNamespace: #namespace
				attrs: [for label, m in self.model if !list.Contains(m.flows, "historic") {
					strings.ToLower(label)
				}]
				attrJoinOn: [
					"entityid",
				]
			}]
		}
	}

	// En el atributo "#sql", se enumera la lista de objetos
	// templates/sql que se deben crear, y los atributos de input
	// que se les deben proporcionar.
	#sql: [label = string]: _
	// Todos los objetos de tipo twin tienen una vista
	// "vector" que extrae las métricas en un formato "homogéneo"
	#sql: vector: {
		metrics: [for _k, _v in self.model if _v.#metric { _k }]
	}

	#sql_template: {for label, data in #sql {
		(label): {
			sql[label]
			input: {
				data
				namespace:  #namespace
				entityType: #entityType
				hasHour:    #hasHour
				hasMinute:  #hasMinute
			}
		}
	}}

	flows: custom_sql: {
		class: "FLOW_RAW"
		sql: sources: custom_sql: {
			documentation: """
				Conjunto de vistas utilitarias para la presentación de
				datos de escenarios identidad y simulaciones.
				"""
			path: "./sql"
			files: [
				"custom_\(#entityType).sql",
			]
			weight: 10
			relations: list.FlattenN([for _, data in #sql_template {
				data.relations
			}], -1)
		}
	}
}
