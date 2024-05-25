El vertical utiliza los siguientes modelos:

1. [AirQualityObserved](#AirQualityObserved)
2. [DayType](#DayType)
3. [OffStreetParking](#OffStreetParking)
4. [RouteIntensity](#RouteIntensity)
5. [RouteSchedule](#RouteSchedule)
6. [Simulation](#Simulation)
7. [SimulationParking](#SimulationParking)
8. [SimulationRoute](#SimulationRoute)
9. [SimulationTraffic](#SimulationTraffic)
10. [Stop](#Stop)
11. [TrafficCongestion](#TrafficCongestion)
12. [TrafficIntensity](#TrafficIntensity)
13. [Trend](#Trend)
14. [Zone](#Zone)

# Entidades Principales

## AirQualityObserved

Calidad del aire observada.

| Atributo    | ngsiType         | dbType                            | description                                                                                                                                                                               | example                                                                        | extra | unit  | range                         |
| ----------- | ---------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----- | ----- | ----------------------------- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                                                  | `"2018-12-10T20:40:23"`                                                        | -     | -     | -                             |
| sourceRef   | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId en a base de datos, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"Parking-01"`                                                                 | -     | -     | -                             |
| sceneRef    | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "N/A" indica que se trata de una vista identidad.                                                            | `"example text"`                                                               | -     | -     | -                             |
| trend       | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                                       | `"Verano"`                                                                     | -     | -     | Verano, Fallas, Otros         |
| dayType     | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                                                  | `"L-J"`                                                                        | -     | -     | L-J, Viernes, Sábado, Domingo |
| name        | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                                          | `"example text"`                                                               | -     | -     | -                             |
| zone        | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                                         | `"Distrito 1"`                                                                 | -     | -     | -                             |
| NO2         | Number           | double precision                  | Dióxido de Nitrógeno                                                                                                                                                                      | `5.0`                                                                          | -     | µg/m3 | -                             |
| PM25        | Number           | double precision                  | Partículas en suspensión inferiores a 2,5 micras                                                                                                                                          | `5.0`                                                                          | -     | µg/m3 | -                             |
| PM10        | Number           | double precision                  | Dióxido de Nitrógeno                                                                                                                                                                      | `5.0`                                                                          | -     | µg/m3 | -                             |
| location    | geo:json         | geometry(Point)                   | Ubicación de la entidad                                                                                                                                                                   | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -     | -                             |
| O3          | Number           | double precision                  | Ozono                                                                                                                                                                                     | `5.0`                                                                          | -     | µg/m3 | -                             |

Ejemplo de `AirQualityObserved` (en NGSIv2):

```json
{
    "id": "C1",
    "type": "AirQualityObserved",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sourceRef": {
        "type": "TextUnrestricted",
        "value": "Parking-01"
    },
    "sceneRef": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "trend": {
        "type": "TextUnrestricted",
        "value": "Verano"
    },
    "dayType": {
        "type": "TextUnrestricted",
        "value": "L-J"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "zone": {
        "type": "TextUnrestricted",
        "value": "Distrito 1"
    },
    "NO2": {
        "type": "Number",
        "value": 5.0
    },
    "PM25": {
        "type": "Number",
        "value": 5.0
    },
    "PM10": {
        "type": "Number",
        "value": 5.0
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [
                3.5,
                24.6
            ]
        }
    },
    "O3": {
        "type": "Number",
        "value": 5.0
    }
}
```

## DayType

Tipo de dia. Este tipo de entidad solo se utiliza para rellenar los selectores en urbo. Tendrá un número fijo de valores: L-J Viernes Sabado Domingo

| Atributo    | ngsiType | dbType                            | description                                              | example                 | extra | unit | range |
| ----------- | -------- | --------------------------------- | -------------------------------------------------------- | ----------------------- | ----- | ---- | ----- |
| TimeInstant | DateTime | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación | `"2018-12-10T20:40:23"` | -     | -    | -     |

Ejemplo de `DayType` (en NGSIv2):

```json
{
    "id": "Sabado",
    "type": "DayType",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    }
}
```

## OffStreetParking

Parking con barrera de acceso

| Atributo          | ngsiType         | dbType                            | description                                                                                                                                                                               | example                                                                        | extra | unit | range                         |
| ----------------- | ---------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----- | ---- | ----------------------------- |
| TimeInstant       | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                                                  | `"2018-12-10T20:40:23"`                                                        | -     | -    | -                             |
| sourceRef         | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId en a base de datos, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"Parking-01"`                                                                 | -     | -    | -                             |
| sceneRef          | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "N/A" indica que se trata de una vista identidad.                                                            | `"example text"`                                                               | -     | -    | -                             |
| trend             | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                                       | `"Verano"`                                                                     | -     | -    | Verano, Fallas, Otros         |
| dayType           | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                                                  | `"L-J"`                                                                        | -     | -    | L-J, Viernes, Sábado, Domingo |
| name              | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                                          | `"example text"`                                                               | -     | -    | -                             |
| hour              | Number           | integer                           | Hora del día a la que corresponde la medida                                                                                                                                               | `15`                                                                           | -     | -    | 0-23                          |
| zone              | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                                         | `"Distrito 1"`                                                                 | -     | -    | -                             |
| capacity          | Number           | double precision                  | Número de plazas totales en el parking                                                                                                                                                    | `5.0`                                                                          | -     | -    | -                             |
| occupationPercent | Number           | double precision                  | Porcentaje de ocupación                                                                                                                                                                   | `23.45`                                                                        | -     | -    | 0-100                         |
| location          | geo:json         | geometry(Point)                   | Ubicación de la entidad                                                                                                                                                                   | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -    | -                             |
| occupation        | Number           | double precision                  | Número de plazas ocupadas                                                                                                                                                                 | `5.0`                                                                          | -     | -    | -                             |

Ejemplo de `OffStreetParking` (en NGSIv2):

```json
{
    "id": "parking-100",
    "type": "OffStreetParking",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sourceRef": {
        "type": "TextUnrestricted",
        "value": "Parking-01"
    },
    "sceneRef": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "trend": {
        "type": "TextUnrestricted",
        "value": "Verano"
    },
    "dayType": {
        "type": "TextUnrestricted",
        "value": "L-J"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "hour": {
        "type": "Number",
        "value": 15
    },
    "zone": {
        "type": "TextUnrestricted",
        "value": "Distrito 1"
    },
    "capacity": {
        "type": "Number",
        "value": 5.0
    },
    "occupationPercent": {
        "type": "Number",
        "value": 23.45
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [
                3.5,
                24.6
            ]
        }
    },
    "occupation": {
        "type": "Number",
        "value": 5.0
    }
}
```

## RouteIntensity

Intensidad de uso ruta. Describe el número de viajeros de una ruta dada una estacionalidad, tipo de día y hora.

| Atributo     | ngsiType         | dbType                            | description                                                                                                                                                                               | example                                                                                     | extra | unit | range                         |
| ------------ | ---------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----- | ---- | ----------------------------- |
| TimeInstant  | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                                                  | `"2018-12-10T20:40:23"`                                                                     | -     | -    | -                             |
| sourceRef    | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId en a base de datos, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"Parking-01"`                                                                              | -     | -    | -                             |
| sceneRef     | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "N/A" indica que se trata de una vista identidad.                                                            | `"example text"`                                                                            | -     | -    | -                             |
| trend        | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                                       | `"Verano"`                                                                                  | -     | -    | Verano, Fallas, Otros         |
| dayType      | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                                                  | `"L-J"`                                                                                     | -     | -    | L-J, Viernes, Sábado, Domingo |
| name         | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                                          | `"example text"`                                                                            | -     | -    | -                             |
| zoneList     | Json             | json                              | Lista de identificadores de la zona o distrito a la que pertenece la entidad                                                                                                              | `["Distrito 1", "Distrito 4"]`                                                              | -     | -    | -                             |
| forwardStops | Number           | integer                           | Número de paradas en el trayecto de ida                                                                                                                                                   | `5`                                                                                         | -     | -    | -                             |
| returnStops  | Number           | integer                           | Número de paradas en el trayecto de vuelta                                                                                                                                                | `5`                                                                                         | -     | -    | -                             |
| forwardTrips | Number           | double precision                  | Número de trayectos de ida                                                                                                                                                                | `5.0`                                                                                       | -     | -    | -                             |
| returnTrips  | Number           | double precision                  | Número de trayectos de vuelta                                                                                                                                                             | `5.0`                                                                                       | -     | -    | -                             |
| location     | geo:json         | geometry(MultiLineString)         | Ubicación de la entidad                                                                                                                                                                   | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[[3.5, 24.6], [33, 44]]]}}` | -     | -    | -                             |
| intensity    | Number           | double precision                  | Número de viajeros                                                                                                                                                                        | `5.0`                                                                                       | -     | -    | -                             |

Ejemplo de `RouteIntensity` (en NGSIv2):

```json
{
    "id": "C1",
    "type": "RouteIntensity",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sourceRef": {
        "type": "TextUnrestricted",
        "value": "Parking-01"
    },
    "sceneRef": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "trend": {
        "type": "TextUnrestricted",
        "value": "Verano"
    },
    "dayType": {
        "type": "TextUnrestricted",
        "value": "L-J"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "zoneList": {
        "type": "Json",
        "value": [
            "Distrito 1",
            "Distrito 4"
        ]
    },
    "forwardStops": {
        "type": "Number",
        "value": 5
    },
    "returnStops": {
        "type": "Number",
        "value": 5
    },
    "forwardTrips": {
        "type": "Number",
        "value": 5.0
    },
    "returnTrips": {
        "type": "Number",
        "value": 5.0
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Line",
            "coordinates": [
                [
                    [
                        3.5,
                        24.6
                    ],
                    [
                        33,
                        44
                    ]
                ]
            ]
        }
    },
    "intensity": {
        "type": "Number",
        "value": 5.0
    }
}
```

## RouteSchedule

Programación de ruta. Describe el número de paradas de una ruta dada una estacionalidad, tipo de día y hora.

| Atributo     | ngsiType         | dbType                            | description                                                                                                                                                                               | example                                                                                     | extra | unit | range                         |
| ------------ | ---------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----- | ---- | ----------------------------- |
| TimeInstant  | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                                                  | `"2018-12-10T20:40:23"`                                                                     | -     | -    | -                             |
| sourceRef    | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId en a base de datos, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"Parking-01"`                                                                              | -     | -    | -                             |
| sceneRef     | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "N/A" indica que se trata de una vista identidad.                                                            | `"example text"`                                                                            | -     | -    | -                             |
| trend        | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                                       | `"Verano"`                                                                                  | -     | -    | Verano, Fallas, Otros         |
| dayType      | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                                                  | `"L-J"`                                                                                     | -     | -    | L-J, Viernes, Sábado, Domingo |
| name         | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                                          | `"example text"`                                                                            | -     | -    | -                             |
| hour         | Number           | integer                           | Hora del día a la que corresponde la medida                                                                                                                                               | `15`                                                                                        | -     | -    | 0-23                          |
| zoneList     | Json             | json                              | Lista de identificadores de la zona o distrito a la que pertenece la entidad                                                                                                              | `["Distrito 1", "Distrito 4"]`                                                              | -     | -    | -                             |
| forwardStops | Number           | integer                           | Número de paradas en el trayecto de ida                                                                                                                                                   | `5`                                                                                         | -     | -    | -                             |
| returnStops  | Number           | integer                           | Número de paradas en el trayecto de vuelta                                                                                                                                                | `5`                                                                                         | -     | -    | -                             |
| forwardTrips | Number           | double precision                  | Número de trayectos de ida                                                                                                                                                                | `5.0`                                                                                       | -     | -    | -                             |
| location     | geo:json         | geometry(MultiLineString)         | Ubicación de la entidad                                                                                                                                                                   | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[[3.5, 24.6], [33, 44]]]}}` | -     | -    | -                             |
| returnTrips  | Number           | double precision                  | Número de trayectos de vuelta                                                                                                                                                             | `5.0`                                                                                       | -     | -    | -                             |

Ejemplo de `RouteSchedule` (en NGSIv2):

```json
{
    "id": "C1",
    "type": "RouteSchedule",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sourceRef": {
        "type": "TextUnrestricted",
        "value": "Parking-01"
    },
    "sceneRef": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "trend": {
        "type": "TextUnrestricted",
        "value": "Verano"
    },
    "dayType": {
        "type": "TextUnrestricted",
        "value": "L-J"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "hour": {
        "type": "Number",
        "value": 15
    },
    "zoneList": {
        "type": "Json",
        "value": [
            "Distrito 1",
            "Distrito 4"
        ]
    },
    "forwardStops": {
        "type": "Number",
        "value": 5
    },
    "returnStops": {
        "type": "Number",
        "value": 5
    },
    "forwardTrips": {
        "type": "Number",
        "value": 5.0
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Line",
            "coordinates": [
                [
                    [
                        3.5,
                        24.6
                    ],
                    [
                        33,
                        44
                    ]
                ]
            ]
        }
    },
    "returnTrips": {
        "type": "Number",
        "value": 5.0
    }
}
```

## Simulation

Instancia de simulación. Recopila la última fecha en la que se ha ejecutado una simulación, o cálculo de vista identidad.

| Atributo    | ngsiType         | dbType                            | description                                              | example                 | extra | unit | range |
| ----------- | ---------------- | --------------------------------- | -------------------------------------------------------- | ----------------------- | ----- | ---- | ----- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación | `"2018-12-10T20:40:23"` | -     | -    | -     |
| sceneref    | TextUnrestricted | text                              | Escenario de simulación que ha creado la entidad         | `"example text"`        | -     | -    | -     |
| name        | TextUnrestricted | text                              | Nombre de la simulación                                  | `"example text"`        | -     | -    | -     |
| description | TextUnrestricted | text                              | Texto descriptivo de la simulación                       | `"example text"`        | -     | -    | -     |

Ejemplo de `Simulation` (en NGSIv2):

```json
{
    "id": "N/A",
    "type": "Simulation",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sceneref": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "description": {
        "type": "TextUnrestricted",
        "value": "example text"
    }
}
```

## SimulationParking

Parámetros de simulación de nuevo parking

| Atributo    | ngsiType         | dbType                            | description                 | example                                                                        | extra | unit | range |
| ----------- | ---------------- | --------------------------------- | --------------------------- | ------------------------------------------------------------------------------ | ----- | ---- | ----- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha de la simulacion      | `"2018-12-10T20:40:23"`                                                        | -     | -    | -     |
| name        | TextUnrestricted | text                              | Nombre del nuevo parking    | `"example text"`                                                               | -     | -    | -     |
| description | TextUnrestricted | text                              | Descripción del parking     | `"example text"`                                                               | -     | -    | -     |
| location    | geo:json         | geometry(Point)                   | Ubicación de la entidad     | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -    | -     |
| capacity    | Number           | integer                           | Capacidad del nuevo parking | `5`                                                                            | -     | -    | -     |
| bias        | TextUnrestricted | text                              | Bias del nuevo parking      | `"example text"`                                                               | -     | -    | -     |
| status      | TextUnrestricted | text                              | Estado de la simulación     | `"example text"`                                                               | -     | -    | -     |

Ejemplo de `SimulationParking` (en NGSIv2):

```json
{
    "id": "tramo-100",
    "type": "SimulationParking",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "description": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [
                3.5,
                24.6
            ]
        }
    },
    "capacity": {
        "type": "Number",
        "value": 5
    },
    "bias": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "status": {
        "type": "TextUnrestricted",
        "value": "example text"
    }
}
```

## SimulationRoute

Parámetros de simulación de nueva línea de transporte

| Atributo    | ngsiType         | dbType                            | description                  | example                                                                                   | extra | unit | range |
| ----------- | ---------------- | --------------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------- | ----- | ---- | ----- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha de la simulacion       | `"2018-12-10T20:40:23"`                                                                   | -     | -    | -     |
| name        | TextUnrestricted | text                              | Nombre de la simulación      | `"example text"`                                                                          | -     | -    | -     |
| description | TextUnrestricted | text                              | Descripción de la simulación | `"example text"`                                                                          | -     | -    | -     |
| location    | geo:json         | geometry(LineString)              | Geometría de la línea        | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[3.5, 24.6], [33, 44]]}}` | -     | -    | -     |
| trips       | Number           | integer                           | Número de viajes diarios     | `5`                                                                                       | -     | -    | -     |
| intensity   | Number           | integer                           | Número de viajeros diarios   | `5`                                                                                       | -     | -    | -     |
| bias        | TextUnrestricted | text                              | Bias de la simulación        | `"example text"`                                                                          | -     | -    | -     |
| status      | TextUnrestricted | text                              | Estado de la simulación      | `"example text"`                                                                          | -     | -    | -     |

Ejemplo de `SimulationRoute` (en NGSIv2):

```json
{
    "id": "tramo-100",
    "type": "SimulationRoute",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "description": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Line",
            "coordinates": [
                [
                    3.5,
                    24.6
                ],
                [
                    33,
                    44
                ]
            ]
        }
    },
    "trips": {
        "type": "Number",
        "value": 5
    },
    "intensity": {
        "type": "Number",
        "value": 5
    },
    "bias": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "status": {
        "type": "TextUnrestricted",
        "value": "example text"
    }
}
```

## SimulationTraffic

Parámetros de simulación de corte o peatonalización de tramo

| Atributo    | ngsiType         | dbType                            | description                      | example                                | extra | unit | range |
| ----------- | ---------------- | --------------------------------- | -------------------------------- | -------------------------------------- | ----- | ---- | ----- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha de la simulacion           | `"2018-12-10T20:40:23"`                | -     | -    | -     |
| name        | TextUnrestricted | text                              | Nombre de la simulación          | `"example text"`                       | -     | -    | -     |
| description | TextUnrestricted | text                              | Descripción de la somulación     | `"example text"`                       | -     | -    | -     |
| location    | TextUnrestricted | json                              | Bounding-box de la zona afectada | `[[0.1111, 0.2222], [0.3333, 0.4444]]` | -     | -    | -     |
| bias        | TextUnrestricted | text                              | Bias de la simulación            | `"example text"`                       | -     | -    | -     |
| status      | TextUnrestricted | text                              | Estado de la simulación          | `"example text"`                       | -     | -    | -     |

Ejemplo de `SimulationTraffic` (en NGSIv2):

```json
{
    "id": "tramo-100",
    "type": "SimulationTraffic",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "description": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "location": {
        "type": "TextUnrestricted",
        "value": [
            [
                0.1111,
                0.2222
            ],
            [
                0.3333,
                0.4444
            ]
        ]
    },
    "bias": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "status": {
        "type": "TextUnrestricted",
        "value": "example text"
    }
}
```

## Stop

Parada - para la creacion de simulaciones de paradas de autobús

| Atributo      | ngsiType         | dbType                            | description                             | example                                                                        | extra | unit | range |
| ------------- | ---------------- | --------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------ | ----- | ---- | ----- |
| TimeInstant   | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora de creación del objeto     | `"2018-12-10T20:40:23"`                                                        | -     | -    | -     |
| name          | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora de creación de la parada   | `"2018-12-10T20:40:23"`                                                        | -     | -    | -     |
| location      | geo:json         | geometry(Point)                   | Coordenadas dfe la parada               | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -    | -     |
| refSimulation | TextUnrestricted | text                              | referencia a la entidad SimulationRoute | `"example text"`                                                               | -     | -    | -     |

Ejemplo de `Stop` (en NGSIv2):

```json
{
    "id": "Stop01",
    "type": "Stop",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "name": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [
                3.5,
                24.6
            ]
        }
    },
    "refSimulation": {
        "type": "TextUnrestricted",
        "value": "example text"
    }
}
```

## TrafficCongestion

Medidor de congestión de tráfico

| Atributo    | ngsiType         | dbType                            | description                                                                                                                                                                               | example                                                                                   | extra | unit | range                         |
| ----------- | ---------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----- | ---- | ----------------------------- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                                                  | `"2018-12-10T20:40:23"`                                                                   | -     | -    | -                             |
| sourceRef   | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId en a base de datos, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"Parking-01"`                                                                            | -     | -    | -                             |
| sceneRef    | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "N/A" indica que se trata de una vista identidad.                                                            | `"example text"`                                                                          | -     | -    | -                             |
| trend       | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                                       | `"Verano"`                                                                                | -     | -    | Verano, Fallas, Otros         |
| dayType     | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                                                  | `"L-J"`                                                                                   | -     | -    | L-J, Viernes, Sábado, Domingo |
| name        | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                                          | `"example text"`                                                                          | -     | -    | -                             |
| hour        | Number           | integer                           | Hora del día a la que corresponde la medida                                                                                                                                               | `15`                                                                                      | -     | -    | 0-23                          |
| minute      | Number           | integer                           | Intervalo de 10 minutos al que corresponde la medida                                                                                                                                      | `20`                                                                                      | -     | -    | 0-50                          |
| zone        | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                                         | `"Distrito 1"`                                                                            | -     | -    | -                             |
| congestion  | Number           | double precision                  | Probabilidad de congestión, en tanto por uno                                                                                                                                              | `0.33`                                                                                    | -     | -    | 0-1                           |
| location    | geo:json         | geometry(LineString)              | Ubicación de la entidad                                                                                                                                                                   | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[3.5, 24.6], [33, 44]]}}` | -     | -    | -                             |

Ejemplo de `TrafficCongestion` (en NGSIv2):

```json
{
    "id": "tramo-100",
    "type": "TrafficCongestion",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sourceRef": {
        "type": "TextUnrestricted",
        "value": "Parking-01"
    },
    "sceneRef": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "trend": {
        "type": "TextUnrestricted",
        "value": "Verano"
    },
    "dayType": {
        "type": "TextUnrestricted",
        "value": "L-J"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "hour": {
        "type": "Number",
        "value": 15
    },
    "minute": {
        "type": "Number",
        "value": 20
    },
    "zone": {
        "type": "TextUnrestricted",
        "value": "Distrito 1"
    },
    "congestion": {
        "type": "Number",
        "value": 0.33
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Line",
            "coordinates": [
                [
                    3.5,
                    24.6
                ],
                [
                    33,
                    44
                ]
            ]
        }
    }
}
```

## TrafficIntensity

Medidor de intensidad de tráfico

| Atributo    | ngsiType         | dbType                            | description                                                                                                                                                                               | example                                                                        | extra | unit | range                         |
| ----------- | ---------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----- | ---- | ----------------------------- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                                                  | `"2018-12-10T20:40:23"`                                                        | -     | -    | -                             |
| sourceRef   | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId en a base de datos, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"Parking-01"`                                                                 | -     | -    | -                             |
| sceneRef    | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "N/A" indica que se trata de una vista identidad.                                                            | `"example text"`                                                               | -     | -    | -                             |
| trend       | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                                       | `"Verano"`                                                                     | -     | -    | Verano, Fallas, Otros         |
| dayType     | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                                                  | `"L-J"`                                                                        | -     | -    | L-J, Viernes, Sábado, Domingo |
| name        | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                                          | `"example text"`                                                               | -     | -    | -                             |
| hour        | Number           | integer                           | Hora del día a la que corresponde la medida                                                                                                                                               | `15`                                                                           | -     | -    | 0-23                          |
| zone        | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                                         | `"Distrito 1"`                                                                 | -     | -    | -                             |
| intensity   | Number           | double precision                  | Intensidad de tráfico estimada en el intervalo                                                                                                                                            | `245`                                                                          | -     | -    | -                             |
| location    | geo:json         | geometry(Point)                   | Ubicación de la entidad                                                                                                                                                                   | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -    | -                             |

Ejemplo de `TrafficIntensity` (en NGSIv2):

```json
{
    "id": "puntoMedida-100",
    "type": "TrafficIntensity",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "sourceRef": {
        "type": "TextUnrestricted",
        "value": "Parking-01"
    },
    "sceneRef": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "trend": {
        "type": "TextUnrestricted",
        "value": "Verano"
    },
    "dayType": {
        "type": "TextUnrestricted",
        "value": "L-J"
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "hour": {
        "type": "Number",
        "value": 15
    },
    "zone": {
        "type": "TextUnrestricted",
        "value": "Distrito 1"
    },
    "intensity": {
        "type": "Number",
        "value": 245
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [
                3.5,
                24.6
            ]
        }
    }
}
```

## Trend

Estacionalidad. PErmite separar diferentes tendencias a lo largo del año. Tendrá un número fijo de valores, por ejemplo: Verano Resto

| Atributo    | ngsiType | dbType                            | description                                              | example                 | extra | unit | range |
| ----------- | -------- | --------------------------------- | -------------------------------------------------------- | ----------------------- | ----- | ---- | ----- |
| TimeInstant | DateTime | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación | `"2018-12-10T20:40:23"` | -     | -    | -     |

Ejemplo de `Trend` (en NGSIv2):

```json
{
    "id": "Verano",
    "type": "Trend",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    }
}
```

## Zone

Zona. Este tipo de entidad solo se utiliza para rellenar los selectores en urbo.

| Atributo    | ngsiType         | dbType                            | description                                              | example                                                                                        | extra | unit | range |
| ----------- | ---------------- | --------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ----- | ---- | ----- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación | `"2018-12-10T20:40:23"`                                                                        | -     | -    | -     |
| zoneId      | Number           | integer                           | ID de zona                                               | `5`                                                                                            | -     | -    | -     |
| name        | TextUnrestricted | text                              | Nombre de zona                                           | `"example text"`                                                                               | -     | -    | -     |
| label       | TextUnrestricted | text                              | Etiqueta para selectores                                 | `"example text"`                                                                               | -     | -    | -     |
| location    | geo:json         | geometry(Polygon)                 | Polígono que delimita la zona                            | `{"type": "geo:json", "value": {"type": "Polygon", "coordinates": [[[3.5, 24.6], [33, 44]]]}}` | -     | -    | -     |

Ejemplo de `Zone` (en NGSIv2):

```json
{
    "id": "Distrito-1",
    "type": "Zone",
    "TimeInstant": {
        "type": "DateTime",
        "value": "2018-12-10T20:40:23"
    },
    "zoneId": {
        "type": "Number",
        "value": 5
    },
    "name": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "label": {
        "type": "TextUnrestricted",
        "value": "example text"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        3.5,
                        24.6
                    ],
                    [
                        33,
                        44
                    ]
                ]
            ]
        }
    }
}
```
