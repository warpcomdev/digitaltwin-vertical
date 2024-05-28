package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

SimulationTraffic: {

	#entityType: "SimulationTraffic"

	description: """
		Parámetros de simulación de corte o peatonalización de tramo
		"""
	exampleId: "tramo-100"

	model: {
		TimeInstant: {
			types.#DateTime
			description: "Fecha de la simulacion"
			flows: ["etl_vectorize"]
		}

		name: {
			types.#TextUnrestricted
			description: "Nombre de la simulación"
			flows: []
		}

		description: {
			types.#TextUnrestricted
			description: "Descripción de la somulación"
			flows: []
		}

		location: {
			types.#Json
			description: "Bounding-box de la zona afectada"
			example: [[0.1111, 0.2222], [0.3333, 0.4444]]
			flows: []
		}

		bias: {
			types.#Text
			description: "Bias de la simulación"
			flows: []
		}

		status: {
			types.#TextUnrestricted
			description: "Estado de la simulación"
			flows: []
		}
	}

	// Peatonalización o corte {
	// 	name
	// 	description
	// 	boundingbox
	// 	bias
	// 	status
	// }

	// lína EMT: {
	// 	name
	// 	description
	// 	trayectos diarios
	// 	viajeros diarios
	// 	bias
	// 	status
	// }

	// Objeto parada:
	// 	name
	// 	latitude
	// 	longitude

	flows: {
		etl_vectorize: {
			class: "FLOW_RAW"
			subscriptions: {
				SimulationParking_etl: {
					documentation: "Subscripción del flujo etl (tipo FLOW_RAW) en modelo SimulationParking"
					description:   "SimulationParking:JENKINS::etl"
					status:        "active"
					subject: {
						entities: [
							{
								idPattern: ".*"
								type:      "SimulationParking"
							},
						]
						condition: {
							attrs: [
								"TimeInstant",
							]
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
								ETL_VECTORIZE_CHANGETYPE: "${changeType}"
							}
							payload: null
						}
					}
				}
			}
		}
	}
}
