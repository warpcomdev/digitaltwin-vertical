package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
	"github.com/telefonicasc/digitaltwin-vertical/schema/templates"

)

SimulationRoute: templates.#Simulation & {

	#entityType:   "SimulationRoute"
	#geometryType: "LineString"

	description: "Parámetros de simulación de nueva línea de transporte"
	exampleId:   "tramo-100"

	model: {
		location: {
			types.#Geometry[#geometryType]
			description: "Geometría de la línea"
			flows: []
		}

		trips: {
			types.#Integer
			description: "Número de viajes diarios"
			flows: []
		}

		intensity: {
			types.#Integer
			description: "Número de viajeros diarios"
			flows: []
		}
	}
}
