package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

TrafficIntensity: templates.#Twin & {

	#entityType:   "TrafficIntensity"
	#geometryType: "Point"
	#hasMinute:    false
	#multiZone:    false

	description: """
		Medidor de intensidad de tráfico
		"""
	exampleId: "puntoMedida-100"

	model: {
		intensity: {
			types.#Double
			description: "Intensidad de tráfico estimada en el intervalo"
			example:     245
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
			intensity: "SUM(intensity)"
		}
		where:    "hour >= 7 and hour < 23"
		withZone: true
	}

	#sql: yesterday: {
		columns: [
			"timeinstant",
			"sourceref",
			"sceneref",
			"trend",
			"daytype",
			"name",
			"zone",
			"intensity",
		]
	}

	#sql: peak: {
		hourFrom:   7
		hourTo:     23
		morningEnd: 15
		columns: [
			"timeinstant",
			"sourceref",
			"sceneref",
			"trend",
			"daytype",
			"name",
			"zone",
		]
		metric: "intensity"
	}
}
