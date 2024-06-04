package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

SimulationParking: templates.#Simulation & {

	#entityType:   "SimulationParking"
	#geometryType: "Point"

	description: """
		Parámetros de simulación de nuevo parking
		"""
	exampleId: "tramo-100"

	model: {
		location: {
			types.#Geometry[#geometryType]
			description: "Ubicación de la entidad"
			flows: []
		}

		capacity: {
			types.#Integer
			description: "Capacidad del nuevo parking"
			flows: []
		}
	}
}
