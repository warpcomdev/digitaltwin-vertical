package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

AirQualityObserved: templates.#Twin & {

	#entityType:   "AirQualityObserved"
	#geometryType: "Point"
	#hasHour:      false
	#hasMinute:    false
	#multiZone:    false

	description: """
		Calidad del aire observada.
		"""
	exampleId: "C1"

	model: {
		NO2: {
			types.#Double
			description: "Dióxido de Nitrógeno"
			unit: "µg/m3",
			flows: ["historic"]
		}

		PM25: {
			types.#Double
			description: "Partículas en suspensión inferiores a 2,5 micras"
			unit: "µg/m3",
			flows: ["historic"]
		}

		PM10: {
			types.#Double
			description: "Dióxido de Nitrógeno"
			unit: "µg/m3",
			flows: ["historic"]
		}

		O3: {
			types.#Double
			description: "Ozono"
			unit: "µg/m3",
			flows: ["historic"]
		}
	}
}
