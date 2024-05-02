package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

RouteSchedule: templates.#Twin & {

	#entityType:   "RouteSchedule"
	#geometryType: "MultiLineString"
	#hasHour:      true
	#hasMinute:    false
	#multiZone:    true

	description: """
		Programación de ruta. Describe el número de paradas de una ruta
		dada una estacionalidad, tipo de día y hora.
		"""
	exampleId: "C1"

	model: {

		forwardTrips: {
			types.#Double
			description: "Número de trayectos de ida"
			flows: ["historic", "lastdata"]
		}

		returnTrips: {
			types.#Double
			description: "Número de trayectos de vuelta"
			flows: ["historic", "lastdata"]
		}

		forwardStops: {
			types.#Integer
			description: "Número de paradas en el trayecto de ida"
			flows: ["historic", "lastdata"]
		}

		returnStops: {
			types.#Integer
			description: "Número de paradas en el trayecto de vuelta"
			flows: ["historic", "lastdata"]
		}
	}
}
