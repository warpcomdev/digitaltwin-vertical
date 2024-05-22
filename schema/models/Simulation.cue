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
	exampleId: "N/A"

	model: [string]: {types.#ModelAttribute}
	model: {

		TimeInstant: {
			types.#DateTime
			description: "Fecha / Hora del cálculo de vista identidad o simulación"
			flows: ["lastdata"]
		}

		sceneref: {
			types.#Text
			description: "Escenario de simulación que ha creado la entidad"
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
		etl_vectorize: {
			class: "FLOW_RAW"
			etls: {
				sources: {
					etl_digitaltwin_vectorize: {
						documentation: "ETL cálculo de escenario"
						path:          "etls/vectorize"
					}
				}
				jobs: {
					etl_digitaltwin_vectorize: {
						job: "etl_digitaltwin_vectorize"
						etl: "etl_digitaltwin_vectorize"
						envFrom: {
							"git":  "telefonicasc/!!{projectName}-project"
							"tag":  "!!{projectTag}"
							"path": "!!{environmentLabel}/etls/configuration/digitaltwin/vectorize"
							"files": [
								"env.json",
							]
						}
						envFromSecrets: {
							"git":  "telefonicasc/!!{projectName}-project"
							"tag":  "!!{projectTag}"
							"path": "!!{environmentLabel}/etls/configuration/digitaltwin/vectorize"
							"files": [
								"env.secrets.json",
							]
						}
						entrypoint: "vectorize.py"
						buildParams: {
							ETL_LOG_LEVEL: {
								type: "choice"
								choices: [
									"INFO",
									"DEBUG",
									"ERROR",
								]
								description: "Por defecto el nivel de las trazas es de INFO"
							}
							ETL_VECTORIZE_SIMULATION_TYPE: {
								type:        "string"
								description: "Tipo de entidad que dispara la simulación"
								default:     ""
							}
							ETL_VECTORIZE_SIMULATION_ID: {
								type:        "string"
								description: "ID de la entidad que dispara la simulación"
								default:     ""
							}
						}
					}
				}
			}
		}
	}
}
