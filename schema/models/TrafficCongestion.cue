package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

TrafficCongestion: templates.#Twin & {

	#entityType:   "TrafficCongestion"
	#geometryType: "LineString"
	#hasMinute:    true
	#multiZone:    false

	description: """
		Medidor de congestión de tráfico
		"""
	exampleId: "tramo-100"

	model: {
		congestion: {
			types.#Double
			description: "Probabilidad de congestión, en tanto por uno"
			range:       "0-1"
			example:     0.33
			flows: ["historic"]
			#metric: true
			#scale:  1
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
			avg_congestion: "AVG(congestion)"
			max_congestion: "MAX(congestion)"
		}
		where: "hour >= 7 AND hour <= 22"
	}

	#sql: hourly: {
		hourFrom: 7
		hourTo:   22
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
			congestion: "AVG(congestion)"
		}
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
			"congestion",
		]
	}

	#sql: peak: {
		hourFrom:   7
		hourTo:     22
		morningEnd: 14
		columns: [
			"timeinstant",
			"sourceref",
			"sceneref",
			"trend",
			"daytype",
			"name",
			"zone",
		]
		metric: "congestion"
	}
}
