package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

DayType: {

	description: """
        Tipo de dia. Este tipo de entidad solo se utiliza para rellenar
        los selectores en urbo. Tendrá un número fijo de valores:

        L-J
        Viernes
        Sabado
        Domingo
        """
	namespace:   "dtwin"
	exampleId:   "Sabado"

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
