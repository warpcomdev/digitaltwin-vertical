package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"
)

SimulationTraffic: templates.#Simulation & {

	#entityType: "SimulationTraffic"

	description: """
		Parámetros de simulación de corte o peatonalización de tramo
		"""
	exampleId: "tramo-100"

	model: {
		location: {
			types.#Json
			description: "Bounding-box de la zona afectada"
			example: [[0.1111, 0.2222], [0.3333, 0.4444]]
			flows: []
		}
	}
}
