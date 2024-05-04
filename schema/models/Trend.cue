package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

Trend: {

	description: """
        Estacionalidad. PErmite separar diferentes tendencias a lo largo del año.
        Tendrá un número fijo de valores, por ejemplo:

        Verano
        Resto
        """
	namespace:   "dtwin"
	exampleId:   "Verano"

	model: [string]: {types.#ModelAttribute}
	model: {

		TimeInstant: {
			types.#DateTime
			description: "Fecha / Hora del cálculo de vista identidad o simulación"
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
