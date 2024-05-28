package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

SimulationParking: {

	#entityType:   "SimulationParking"
	#geometryType: "Point"

	description: """
		Parámetros de simulación de nuevo parking
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
			description: "Nombre del nuevo parking"
			flows: []
		}

		description: {
			types.#TextUnrestricted
			description: "Descripción del parking"
			flows: []
		}

		location: {
			types.#Geometry[#geometryType]
			description: "Ubicación de la entidad"
			flows: []
		}

		capacity: {
			types.#Integer
			description: "Capacidad del nuevo parking"
			flows: []
		}

		bias: {
			types.#Text
			description: "Bias del nuevo parking"
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
