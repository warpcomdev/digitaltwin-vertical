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

		forwardTrips: {
			types.#Double
			description: "Número de trayectos de ida"
			flows: ["historic"]
			#metric: true
		}

		returnTrips: {
			types.#Double
			description: "Número de trayectos de vuelta"
			flows: ["historic"]
			#metric: true
		}

		intensity: {
			types.#Double
			description: "Número de viajeros"
			flows: ["historic"]
			#metric: true
		}
	}

	#sql: daily: {
		columns: [
			"timeinstant",
			"sourceref",
			"sceneref",
			"trend",
			"daytype",
			"name",
			"zone",
		]
		aggregations: {
			intensity_per_trip: "sum(t.intensity) / sum(t.forwardtrips + t.returntrips)::double precision"
			intensity_per_stop: "sum(t.intensity) / sum(t.forwardtrips * t.forwardstops + t.returntrips * t.returnstops)"
		}
		where: """
			intensity IS NOT NULL AND
			forwardtrips IS NOT NULL AND
			returntrips IS NOT NULL AND
			forwardstops IS NOT NULL AND
			returnstops IS NOR NULL AND
			(forwardtrips + returntrips) > 0 AND
			(forwardstops + returnstops) > 0
			"""
	}
}
