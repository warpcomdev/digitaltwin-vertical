package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

RouteIntensity: templates.#Twin & {

	#entityType:   "RouteIntensity"
	#geometryType: "MultiLineString"
	#hasHour:      false
	#hasMinute:    false
	#multiZone:    true

	description: """
		Intensidad de uso ruta. Describe el número de viajeros 
		de una ruta dada una estacionalidad, tipo de día y hora.
		"""
	exampleId: "C1"

	model: {

		forwardTrips: {
			types.#Double
			description: "Número de trayectos de ida"
			flows: ["historic"]
		}

		returnTrips: {
			types.#Double
			description: "Número de trayectos de vuelta"
			flows: ["historic"]
		}

		forwardStops: {
			types.#Integer
			description: "Número de paradas en el trayecto de ida"
			flows: ["historic"]
		}

		returnStops: {
			types.#Integer
			description: "Número de paradas en el trayecto de vuelta"
			flows: ["historic"]
		}

		intensity: {
			types.#Double
			description: "Número de viajeros"
			flows: ["historic"]
			#metric: true
		}
	}
}
