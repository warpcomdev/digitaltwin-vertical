package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

Stop: {

	#entityType:   "Stop"
	#geometryType: "Point"

	description: "Parada - para la creacion de simulaciones de paradas de autobús"
	namespace:   "dtwin"
	exampleId:   "Stop01"

	model: [string]: {types.#ModelAttribute}
	model: {

		TimeInstant: {
			types.#DateTime
			description: "Fecha / Hora de creación del objeto"
			flows: []
		}

		name: {
			types.#DateTime
			description: "Fecha / Hora de creación de la parada"
			flows: []
		}

		location: {
			types.#Geometry[#geometryType]
			description: "Coordenadas dfe la parada"
			flows: []
		}

		refSimulation: {
			types.#Text
			description: "referencia a la entidad SimulationRoute"
			flows: []
		}
	}

	flows: {}
}
