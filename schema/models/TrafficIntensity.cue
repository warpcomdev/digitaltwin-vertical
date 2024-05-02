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
			flows: ["historic", "lastdata"]
		}
	}
}
