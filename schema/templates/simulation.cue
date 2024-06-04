package templates

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

#Simulation: {

	#entityType: string // Para reutilizar el tipo de entidad

	description: string
	exampleId:   string

	model: [string]: {
		types.#ModelAttribute
	}

	model: {
		TimeInstant: {
			types.#DateTime
			description: "Fecha de la simulacion"
			flows: ["etl_vectorize"]
		}

		name: {
			types.#TextUnrestricted
			description: "Nombre de la nueva simulación"
			flows: []
		}

		description: {
			types.#TextUnrestricted
			description: "Descripción de la nueva simulación"
			flows: []
		}

		bias: {
			types.#Text
			description: "Bias a aplicar en la simulación"
			flows: []
		}

		status: {
			types.#TextUnrestricted
			description: "Estado de la simulación"
			flows: []
		}
	}

	flows: {
		etl_vectorize: {
			class: "FLOW_RAW"
			subscriptions: {
				trigger_etl: {
					documentation: "Subscripción del flujo etl_vectorize (tipo FLOW_RAW) en modelo \(#entityType)"
					description:   "\(#entityType):JENKINS::etl_vectorize_run"
					status:        "active"
					subject: {
						entities: [
							{
								idPattern: ".*"
								type:      #entityType
							},
						]
						condition: {
							attrs: [
								"TimeInstant",
							]
							alterationTypes: ["entityCreate", "entityUpdate", "entityChange", "entityDelete"]
						}
					}
					notification: {
						attrs: [
							"TimeInstant",
						]
						httpCustom: {
							url: "JENKINS/etl_digitaltwin_vectorize/buildWithParameters"
							headers: {
								Authorization: "Basic !!{JENKINS_BASIC_AUTH}"
							}
							qs: {
								ETL_VECTORIZE_SIMULATION_TYPE: "${type}"
								ETL_VECTORIZE_SIMULATION_ID:   "${id}"
								ETL_VECTORIZE_CHANGETYPE:      "${alterationType}"
							}
							payload: null
						}
					}
				}
			}
		}
	}
}
