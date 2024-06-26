package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

OffStreetParking: templates.#Twin & {

	#entityType:   "OffStreetParking"
	#geometryType: "Point"
	#hasMinute:    false
	#multiZone:    false

	description: """
		Parking con barrera de acceso
		"""
	exampleId: "parking-100"

	model: {

		capacity: {
			types.#Double
			description: "Número de plazas totales en el parking"
			flows: ["historic", "lastdata"]
		}

		occupationPercent: {
			types.#Double
			description: "Porcentaje de ocupación"
			range:       "0-100"
			example:     23.45
			flows: ["historic"]
			#metric: true
			#scale:  100
		}

		occupation: {
			types.#Double
			description: "Número de plazas ocupadas"
			flows: ["historic"]
			#calc: "capacity * occupationPercent / 100.0"
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
			capacity:          "MAX(capacity)"
			occupation:        "AVG(occupation)"
			occupationPercent: "SUM(occupation) / SUM(capacity)::double precision"
		}
		where: "hour >= 7 AND hour < 23"
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
			"capacity",
			"occupation",
			"occupationPercent",
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
		metric: "occupationPercent"
	}

	#sql: freq: {
		columns: [
			"timeinstant",
			"sourceref",
			"sceneref",
			"trend",
			"daytype",
			"name",
			"zone",
		]
		metric: "occupationPercent"
		ranges: {
			"tramo_0": 30
			"tramo_1": 50
			"tramo_2": 70
			"tramo_3": 90
		}
		other:  "tramo_4"
		metric: "occupationPercent"
	}
}
