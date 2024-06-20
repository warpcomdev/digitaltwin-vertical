package models

Transversal: {

	description: "Paneles de la vertical de gemelo digital"
	namespace:   "dtwin"
	model: {}

	flows: {
		transversal: {
			class: "FLOW_RAW"
			panels: {
				sources: {
					base: {
						path: "panels"
						files: [
							"gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion.json",
							"gemelo-digital-tablero-simulacion-nueva-linea-emt.json",
							"gemelo-digital-tablero-simulacion-nuevo-parking.json",
							"gemelo-digital-tablero-simulacion-peatonalizacion-de-calle.json",
							"gemelo-digital-panel-comparacion.json",
							"gemelo-digital-vista-identidad.json",
							"gemelo-digital-vista-simulada-city.json",
							"gemelo-digital-vista-simulada.json",
							"gemelo-digital-vista-simulada-parking.json",
							"gemelo-digital-vista-simulada-publictransport.json",
							"gemelo-digital-vista-simulada-traffic.json",
							"gemelo-digital-vista-identidad-city.json",
							"gemelo-digital-vista-identidad-parking.json",
							"gemelo-digital-vista-identidad-publictransport.json",
							"gemelo-digital-vista-identidad-traffic.json",
						]
					}
				}
			}
			verticals: {
				GemeloDigital: {
					panels: [
						"gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion",
						"gemelo-digital-tablero-simulacion-nueva-linea-emt",
						"gemelo-digital-tablero-simulacion-nuevo-parking",
						"gemelo-digital-tablero-simulacion-peatonalizacion-de-calle",
						"gemelo-digital-panel-comparacion",
						"gemelo-digital-vista-identidad",
						"gemelo-digital-vista-simulada-city",
						"gemelo-digital-vista-simulada",
						"gemelo-digital-vista-simulada-parking",
						"gemelo-digital-vista-simulada-publictransport",
						"gemelo-digital-vista-simulada-traffic",
						"gemelo-digital-vista-identidad-city",
						"gemelo-digital-vista-identidad-parking",
						"gemelo-digital-vista-identidad-publictransport",
						"gemelo-digital-vista-identidad-traffic",
					]
					slug: "gemelo-digital-vertical"
				}
			}
		}
	}
}
