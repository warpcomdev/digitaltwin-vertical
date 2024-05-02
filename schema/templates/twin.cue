package templates

import (
	"list"
	"strings"

	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

#Twin: self={

	#entityType:   string
	#hasHour:      bool | *true
	#hasMinute:    bool | *false
	#multiZone:    bool | *false
	#geometryType: *"Point" | "Line" | "MultiLine" | "Polygon" | "MultiPolygon"

	description: string
	namespace:   "dtwin"
	exampleId:   string

	model: [string]: {types.#ModelAttribute}
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
				"""
			flows: ["historic", "lastdata"]
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
			#keys: {
				sourceRef: true
				sceneRef:  true
				trend:     true
				dayType:   true
				...
			}
			if #hasHour {
				#keys: hour: true
			}
			if #hasMinute {
				#keys: minute: true
			}
			attrs: [for label, _ in #keys {label}]
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
				attrs: ["TimeInstant"] + self.#aspects.singleton.attrs
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
			#tableName: strings.ToLower(self.#entityType)
			leftModel: {
				name:            #tableName
				entityNamespace: self.namespace
				attrs: [
					"entityid", "entityType", "fiwareservicepath", "recvtime",
				] + [for label, m in self.model if list.Contains(m.flows, "historic") {
					strings.ToLower(label)
				}]
				attrJoinOn: ["entityid"]
			}
			rightModel: [{
				name:            "\(#tableName)_lastdata"
				entityNamespace: self.namespace
				attrs: [for label, m in self.model if !list.Contains(m.flows, "historic") {
					strings.ToLower(label)
				}]
				attrJoinOn: [
					"entityid",
				]
			}]
		}
	}
}
