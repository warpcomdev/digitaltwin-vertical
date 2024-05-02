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
			description: "Número de plazas disponibles en el parking"
			flows: ["historic", "lastdata"]
		}

		occupationPercent: {
			types.#Double
			description: "Porcentaje de ocupación"
			range:       "0-100"
			example:     23.45
			flows: ["historic", "lastdata"]
		}

		occupation: {
			types.#Double
			description: "Número de plazas ocupadas"
			flows: ["historic", "lastdata"]
		}
	}
}
