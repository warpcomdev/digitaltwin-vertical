package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

TrafficCongestion: templates.#Twin & {

	#entityType:   "TrafficCongestion"
	#geometryType: "Point"
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
			flows: ["historic", "lastdata"]
		}
	}

	#sql: daily: {
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
