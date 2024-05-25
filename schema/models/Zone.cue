package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

Zone: {

	description: """
		Zona. Este tipo de entidad solo se utiliza para rellenar
		los selectores en urbo.
		"""
	namespace: "dtwin"
	exampleId: "Distrito-1"

	model: [string]: {types.#ModelAttribute}
	model: {

		TimeInstant: {
			types.#DateTime
			description: "Fecha / Hora del cálculo de vista identidad o simulación"
			flows: ["lastdata"]
		}

		zoneId: {
			types.#Integer
			description: "ID de zona"
			flows: ["lastdata"]
		}

		name: {
			types.#Text
			description: "Nombre de zona"
			flows: ["lastdata"]
		}

		label: {
			types.#Text
			description: "Etiqueta para selectores"
			flows: ["lastdata"]
		}

		location: {
			types.#Geometry.Geometry
			description: "Polígono que delimita la zona"
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
