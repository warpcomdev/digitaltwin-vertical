package templates

import (
	"list"
	"strings"
	"encoding/json"

	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	sql_templates "github.com/telefonicasc/digitaltwin-vertical/schema/templates/sql"
)

#Twin: self={

	#entityType: string // Para reutilizar el tipo de entidad

	#hasHour: bool | *true // True si la vista identidad tiene horas

	#hasMinute: bool | *false // True si la vista identidad tiene minutos

	#multiZone:    bool | *false // True si la entidad ocupa múltiples zonas
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
				Reemplaza al entityId en a base de datos, ya que esta entidad
				es *singleton* y su ID en base de datos se ve sobrescrito
				por una composición de los campos únicos.
				"""
			flows: ["historic", "lastdata"]
			example: "Parking-01"
		}

		sceneRef: {
			types.#Text
			description: """
				ID del escenario de simulación.
				Identifica la simulación realizada. El valor "NA"
				indica que se trata de una vista identidad.
				"""
			flows: ["historic"]
		}

		trend: {
			types.#Text
			description: "Estacionalidad o tendencia para la que se ha calculado el escenario"
			flows: ["historic"]
			#range: ["Verano", "Fallas", "Otros"]
		}

		dayType: {
			types.#Text
			description: "Tipo de día al que corresponde la medida"
			flows: ["historic"]
			#range: ["L-J", "Viernes", "Sábado", "Domingo"]
		}

		if #hasHour {
			hour: {
				types.#Integer
				description: "Hora del día a la que corresponde la medida"
				flows: ["historic"]
				range:   "0-23"
				example: 15
			}
		}

		if #hasMinute {
			minute: {
				types.#Integer
				description: "Intervalo de 10 minutos al que corresponde la medida"
				flows: ["historic"]
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
				flows: ["lastdata"]
			}
		}

		if #multiZone {
			zoneList: {
				types.#Array
				description: "Lista de identificadores de la zona o distrito a la que pertenece la entidad"
				example: ["Distrito 1", "Distrito 4"]
				flows: ["lastdata"]
			}
		}
	}

	// Columnas que forman parte de la clave única del objeto.
	#unique: [...string]
	if !#hasHour && !#hasMinute {
		#unique: ["sceneRef", "trend", "dayType"]
	}
	if #hasHour && !#hasMinute {
		#unique: ["sceneRef", "trend", "dayType", "hour"]
	}
	if #hasMinute {
		#unique: ["sceneRef", "trend", "dayType", "hour", "minute"]
	}

	flows: {

		// Flujo histórico customizado. Tanto la primary key
		// como la condición de disparo de la notificación están
		// personalizadas para el caso de uso.
		historic: {
			class:    "FLOW_HISTORIC"
			endpoint: "HISTORIC"
			pk: ["entityid", "timeinstant"] + #unique
			dbIndexes: {
				scene: "(timeinstant, sceneRef)"
			}
			condition: {
				attrs: ["sourceRef", "TimeInstant"] + #unique
				expression: q: "sceneRef"
			}
			replaceId: ["sourceRef"]
		}

		// Flujo lastdata customizado. Básicamente es la dimensión
		// que contiene las coordenadas y nombres descriptivos.
		lastdata: {
			class:    "FLOW_LASTDATA"
			endpoint: "LASTDATA"
			condition: {
				attrs: ["TimeInstant", "sourceRef"]
				// No quiero que me borre las filas de la tabla,
				// cuando se borren las entidades. Me aseguro de
				// excluir el alterationType onDelete.
				alterationTypes: [
					"entityUpdate",
					"entityCreate",
				]
			}
			replaceId: ["sourceRef"]
		}

		// Flujo join de datos unidos
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

		// Vista de simulación. Permite quedarse con
		// las columnas resultado concretas de una simulacion
		// particular.
		sim: {
			class:      "FLOW_JOIN_VIEW"
			#tableName: strings.ToLower(#entityType)
			leftModel: {
				name:            "simulation_lastdata"
				entityNamespace: #namespace
				attrs: [
					"timeinstant",
				]
				attrJoinOn: ["entityId", "timeinstant"]
			}
			rightModel: [{
				name:            "\(#tableName)_join"
				entityNamespace: #namespace
				attrs: [
					"entityid", "entitytype", "recvtime", "fiwareservicepath",
				] + [for label, m in self.model if label != "TimeInstant" {
					strings.ToLower(label)
				}]
				attrJoinOn: ["sceneRef", "timeinstant"]
			}]
		}
	}

	// En el atributo "#sql", se enumera la lista de objetos
	// templates/sql que se deben crear, y los atributos de input
	// que se les deben proporcionar.
	#sql: [label = string]: _

	#export: sql: {for label, data in #sql {
		(label): {
			sql_templates[label]
			input: {
				data
				namespace:  #namespace
				entityType: #entityType
				hasHour:    #hasHour
				hasMinute:  #hasMinute
				multiZone:  #multiZone
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
			relations: list.FlattenN([for _, data in #export.sql {
				data.relations
			}], -1)
		}
	}

	// Todos los objetos de tipo twin tienen un atributo #meta
	// que recoge información necesaria para que luego la ETL
	// pueda utilizar los datos de cualquier datasource
	#export: meta: all: {
		input: {
			dimensions: ["sourceRef"] + #unique
			metrics: [for _k, _v in self.model if _v.#metric {_k}]
			hasHour:   #hasHour
			hasMinute: #hasMinute
			multiZone: #multiZone

			namespace:  #namespace
			entityType: #entityType
			tableName:  "\(namespace)_\(strings.ToLower(entityType))_sim"
		}

		// Genera un json con todos los metadatos
		template: "\(json.Marshal(input))"
	}
}
