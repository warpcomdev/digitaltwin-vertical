package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

Simulation: {

	description: """
		Instancia de simulación. Recopila la última fecha en la que se ha ejecutado
		una simulación, o cálculo de vista identidad.
		"""
	namespace: "dtwin"
	exampleId: "NA"

	model: [string]: {types.#ModelAttribute}
	model: {

		TimeInstant: {
			types.#DateTime
			description: "Fecha / Hora del cálculo de vista identidad o simulación"
			flows: ["lastdata"]
		}

		description: {
			types.#TextUnrestricted
			description: "Texto descriptivo de la simulación"
			flows: ["lastdata"]
		}
	}

	flows: {
		lastdata: {
			class:    "FLOW_LASTDATA"
			endpoint: "LASTDATA"
		}
	}
}
