El vertical utiliza los siguientes modelos:

1. [DayType](#DayType)
2. [OffStreetParking](#OffStreetParking)
3. [RouteIntensity](#RouteIntensity)
4. [RouteSchedule](#RouteSchedule)
5. [TrafficCongestion](#TrafficCongestion)
6. [TrafficIntensity](#TrafficIntensity)
7. [Trend](#Trend)
8. [Zone](#Zone)

# Entidades Principales

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

| Atributo          | ngsiType         | dbType                            | description                                                                                                                                                            | example                                                                        | extra | unit | range                         |
| ----------------- | ---------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----- | ---- | ----------------------------- |
| TimeInstant       | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                               | `"2018-12-10T20:40:23"`                                                        | -     | -    | -                             |
| sourceRef         | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"example text"`                                                               | -     | -    | -                             |
| sceneRef          | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "NA" indica que se trata de una vista identidad.                                          | `"example text"`                                                               | -     | -    | -                             |
| trend             | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                    | `"Verano"`                                                                     | -     | -    | Verano, Fallas, Otros         |
| dayType           | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                               | `"L-J"`                                                                        | -     | -    | L-J, Viernes, Sábado, Domingo |
| name              | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                       | `"example text"`                                                               | -     | -    | -                             |
| hour              | Number           | int                               | Hora del día a la que corresponde la medida                                                                                                                            | `15`                                                                           | -     | -    | 0-23                          |
| zone              | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                      | `"Distrito 1"`                                                                 | -     | -    | -                             |
| capacity          | Number           | double precision                  | Número de plazas disponibles en el parking                                                                                                                             | `5.0`                                                                          | -     | -    | -                             |
| occupationPercent | Number           | double precision                  | Porcentaje de ocupación                                                                                                                                                | `23.45`                                                                        | -     | -    | 0-100                         |
| location          | geo:json         | geometry(Point)                   | Ubicación de la entidad                                                                                                                                                | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -    | -                             |
| occupation        | Number           | double precision                  | Número de plazas ocupadas                                                                                                                                              | `5.0`                                                                          | -     | -    | -                             |

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
        "value": "example text"
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

Programación de ruta. Describe el número de paradas de una ruta dada una estacionalidad, tipo de día y hora.

| Atributo     | ngsiType         | dbType                            | description                                                                                                                                                            | example                                                                                     | extra | unit | range                         |
| ------------ | ---------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----- | ---- | ----------------------------- |
| TimeInstant  | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                               | `"2018-12-10T20:40:23"`                                                                     | -     | -    | -                             |
| sourceRef    | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"example text"`                                                                            | -     | -    | -                             |
| sceneRef     | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "NA" indica que se trata de una vista identidad.                                          | `"example text"`                                                                            | -     | -    | -                             |
| trend        | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                    | `"Verano"`                                                                                  | -     | -    | Verano, Fallas, Otros         |
| dayType      | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                               | `"L-J"`                                                                                     | -     | -    | L-J, Viernes, Sábado, Domingo |
| name         | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                       | `"example text"`                                                                            | -     | -    | -                             |
| zoneList     | Json             | json                              | Lista de identificadores de la zona o distrito a la que pertenece la entidad                                                                                           | `["Distrito 1", "Distrito 4"]`                                                              | -     | -    | -                             |
| forwardTrips | Number           | double precision                  | Número de trayectos de ida                                                                                                                                             | `5.0`                                                                                       | -     | -    | -                             |
| returnTrips  | Number           | double precision                  | Número de trayectos de vuelta                                                                                                                                          | `5.0`                                                                                       | -     | -    | -                             |
| forwardStops | Number           | int                               | Número de paradas en el trayecto de ida                                                                                                                                | `5`                                                                                         | -     | -    | -                             |
| returnStops  | Number           | int                               | Número de paradas en el trayecto de vuelta                                                                                                                             | `5`                                                                                         | -     | -    | -                             |
| location     | geo:json         | geometry(MultiLineString)         | Ubicación de la entidad                                                                                                                                                | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[[3.5, 24.6], [33, 44]]]}}` | -     | -    | -                             |
| intensity    | Number           | double precision                  | Número de viajeros                                                                                                                                                     | `5.0`                                                                                       | -     | -    | -                             |

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
        "value": "example text"
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
    "forwardTrips": {
        "type": "Number",
        "value": 5.0
    },
    "returnTrips": {
        "type": "Number",
        "value": 5.0
    },
    "forwardStops": {
        "type": "Number",
        "value": 5
    },
    "returnStops": {
        "type": "Number",
        "value": 5
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

| Atributo     | ngsiType         | dbType                            | description                                                                                                                                                            | example                                                                                     | extra | unit | range                         |
| ------------ | ---------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----- | ---- | ----------------------------- |
| TimeInstant  | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                               | `"2018-12-10T20:40:23"`                                                                     | -     | -    | -                             |
| sourceRef    | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"example text"`                                                                            | -     | -    | -                             |
| sceneRef     | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "NA" indica que se trata de una vista identidad.                                          | `"example text"`                                                                            | -     | -    | -                             |
| trend        | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                    | `"Verano"`                                                                                  | -     | -    | Verano, Fallas, Otros         |
| dayType      | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                               | `"L-J"`                                                                                     | -     | -    | L-J, Viernes, Sábado, Domingo |
| name         | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                       | `"example text"`                                                                            | -     | -    | -                             |
| hour         | Number           | int                               | Hora del día a la que corresponde la medida                                                                                                                            | `15`                                                                                        | -     | -    | 0-23                          |
| zoneList     | Json             | json                              | Lista de identificadores de la zona o distrito a la que pertenece la entidad                                                                                           | `["Distrito 1", "Distrito 4"]`                                                              | -     | -    | -                             |
| forwardTrips | Number           | double precision                  | Número de trayectos de ida                                                                                                                                             | `5.0`                                                                                       | -     | -    | -                             |
| returnTrips  | Number           | double precision                  | Número de trayectos de vuelta                                                                                                                                          | `5.0`                                                                                       | -     | -    | -                             |
| forwardStops | Number           | int                               | Número de paradas en el trayecto de ida                                                                                                                                | `5`                                                                                         | -     | -    | -                             |
| location     | geo:json         | geometry(MultiLineString)         | Ubicación de la entidad                                                                                                                                                | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[[3.5, 24.6], [33, 44]]]}}` | -     | -    | -                             |
| returnStops  | Number           | int                               | Número de paradas en el trayecto de vuelta                                                                                                                             | `5`                                                                                         | -     | -    | -                             |

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
        "value": "example text"
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
    "forwardTrips": {
        "type": "Number",
        "value": 5.0
    },
    "returnTrips": {
        "type": "Number",
        "value": 5.0
    },
    "forwardStops": {
        "type": "Number",
        "value": 5
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
    "returnStops": {
        "type": "Number",
        "value": 5
    }
}
```

## TrafficCongestion

Medidor de congestión de tráfico

| Atributo    | ngsiType         | dbType                            | description                                                                                                                                                            | example                                                                                   | extra | unit | range                         |
| ----------- | ---------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----- | ---- | ----------------------------- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                               | `"2018-12-10T20:40:23"`                                                                   | -     | -    | -                             |
| sourceRef   | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"example text"`                                                                          | -     | -    | -                             |
| sceneRef    | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "NA" indica que se trata de una vista identidad.                                          | `"example text"`                                                                          | -     | -    | -                             |
| trend       | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                    | `"Verano"`                                                                                | -     | -    | Verano, Fallas, Otros         |
| dayType     | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                               | `"L-J"`                                                                                   | -     | -    | L-J, Viernes, Sábado, Domingo |
| name        | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                       | `"example text"`                                                                          | -     | -    | -                             |
| hour        | Number           | int                               | Hora del día a la que corresponde la medida                                                                                                                            | `15`                                                                                      | -     | -    | 0-23                          |
| minute      | Number           | int                               | Intervalo de 10 minutos al que corresponde la medida                                                                                                                   | `20`                                                                                      | -     | -    | 0-50                          |
| zone        | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                      | `"Distrito 1"`                                                                            | -     | -    | -                             |
| congestion  | Number           | double precision                  | Probabilidad de congestión, en tanto por uno                                                                                                                           | `0.33`                                                                                    | -     | -    | 0-1                           |
| location    | geo:json         | geometry(LineString)              | Ubicación de la entidad                                                                                                                                                | `{"type": "geo:json", "value": {"type": "Line", "coordinates": [[3.5, 24.6], [33, 44]]}}` | -     | -    | -                             |

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
        "value": "example text"
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

| Atributo    | ngsiType         | dbType                            | description                                                                                                                                                            | example                                                                        | extra | unit | range                         |
| ----------- | ---------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----- | ---- | ----------------------------- |
| TimeInstant | DateTime         | timestamp with time zone NOT NULL | Fecha / Hora del cálculo de vista identidad o simulación                                                                                                               | `"2018-12-10T20:40:23"`                                                        | -     | -    | -                             |
| sourceRef   | TextUnrestricted | text                              | ID de entidad original. Reemplaza al entityId, ya que esta entidad es *singleton* y su ID en base de datos se ve sobrescrito por una composición de los campos únicos. | `"example text"`                                                               | -     | -    | -                             |
| sceneRef    | TextUnrestricted | text                              | ID del escenario de simulación. Identifica la simulación realizada. El valor "NA" indica que se trata de una vista identidad.                                          | `"example text"`                                                               | -     | -    | -                             |
| trend       | TextUnrestricted | text                              | Estacionalidad o tendencia para la que se ha calculado el escenario                                                                                                    | `"Verano"`                                                                     | -     | -    | Verano, Fallas, Otros         |
| dayType     | TextUnrestricted | text                              | Tipo de día al que corresponde la medida                                                                                                                               | `"L-J"`                                                                        | -     | -    | L-J, Viernes, Sábado, Domingo |
| name        | TextUnrestricted | text                              | Nombre descriptivo de la entidad                                                                                                                                       | `"example text"`                                                               | -     | -    | -                             |
| hour        | Number           | int                               | Hora del día a la que corresponde la medida                                                                                                                            | `15`                                                                           | -     | -    | 0-23                          |
| zone        | TextUnrestricted | text                              | Identificador de la zona o distrito a la que pertenece la entidad                                                                                                      | `"Distrito 1"`                                                                 | -     | -    | -                             |
| intensity   | Number           | double precision                  | Intensidad de tráfico estimada en el intervalo                                                                                                                         | `245`                                                                          | -     | -    | -                             |
| location    | geo:json         | geometry(Point)                   | Ubicación de la entidad                                                                                                                                                | `{"type": "geo:json", "value": {"type": "Point", "coordinates": [3.5, 24.6]}}` | -     | -    | -                             |

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
        "value": "example text"
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
| zoneId      | Number           | int                               | ID de zona                                               | `5`                                                                                            | -     | -    | -     |
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
