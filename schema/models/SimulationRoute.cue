package models

import (
	"github.com/telefonicasc/digitaltwin-vertical/schema/types"
)

SimulationRoute: {

	#entityType:   "SimulationRoute"
	#geometryType: "LineString"

	description: "Parámetros de simulación de nueva línea de transporte"
	exampleId:   "tramo-100"

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
			description: "Descripción de la simulación"
			flows: []
		}

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
				simulationroute_etl: {
					documentation: "Subscripción del flujo etl (tipo FLOW_RAW) en modelo SimulationRoute"
					description:   "SimulationRoute:JENKINS::etl"
					status:        "active"
					subject: {
						entities: [
							{
								idPattern: ".*"
								type:      "SimulationRoute"
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
							}
							payload: null
						}
					}
				}
			}
		}
	}
}
