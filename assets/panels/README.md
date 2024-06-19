# Paneles del vertical GemeloDigital

## Índice de paneles

### Paneles principales

| Título                                                  | Panel                                                                                                                               | Descripción                                                                         |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Tablero de simulación: Corte de calle de larga duración | [gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion](#panel-tablero-de-simulación-corte-de-calle-de-larga-duración) | Tablero de simulación del Gemelo Digital - Pestaña corte de calle de larga duración |
| Tablero de simulación: Nueva línea EMT                  | [gemelo-digital-tablero-simulacion-nueva-linea-emt](#panel-tablero-de-simulación-nueva-línea-emt)                                   | Tablero de simulación del Gemelo Digital - Pestaña nueva línea EMT                  |
| Tablero de simulación: Nuevo parking                    | [gemelo-digital-tablero-simulacion-nuevo-parking](#panel-tablero-de-simulación-nuevo-parking)                                       | Tablero de simulación del Gemelo Digital - Pestaña nuevo parking                    |
| Tablero de simulación: Peatonalización de calle         | [gemelo-digital-tablero-simulacion-peatonalizacion-de-calle](#panel-tablero-de-simulación-peatonalización-de-calle)                 | Tablero de simulación del Gemelo Digital - Pestaña peatonalización de calle         |
| Panel comparación                                       | [gemelo-digital-panel-comparacion](#panel-panel-comparación)                                                                        | Panel de demo del Gemelo Digital. Vista comparativa                                 |
| Vista identidad: Estado general                         | [gemelo-digital-vista-identidad](#panel-vista-identidad-estado-general)                                                             | Panel de demo del Gemelo Digital                                                    |
| Vista simulada: Urbanismo                               | [gemelo-digital-vista-simulada-city](#panel-vista-simulada-urbanismo)                                                               | Panel de demo del Gemelo Digital. Vista simulada. Pestaña urbanismo.                |
| Vista simulada: Estado general                          | [gemelo-digital-vista-simulada](#panel-vista-simulada-estado-general)                                                               | Panel de demo del Gemelo Digital. Vista simulada                                    |
| Vista simulada: Parking                                 | [gemelo-digital-vista-simulada-parking](#panel-vista-simulada-parking)                                                              | Panel de demo del Gemelo Digital. Vista simulada. Pestaña parking.                  |
| Vista simulada: Transporte público                      | [gemelo-digital-vista-simulada-publictransport](#panel-vista-simulada-transporte-público)                                           | Panel de demo del Gemelo Digital. Vista simulada. Pestaña transporte público        |
| Vista simulada: Tráfico                                 | [gemelo-digital-vista-simulada-traffic](#panel-vista-simulada-tráfico)                                                              | Panel de demo del Gemelo Digital. Vista simulada. Pestaña tráfico                   |
| Vista identidad: Urbanismo                              | [gemelo-digital-vista-identidad-city](#panel-vista-identidad-urbanismo)                                                             | Panel de demo del Gemelo Digital - Pestaña Urbanismo                                |
| Vista identidad: Parking                                | [gemelo-digital-vista-identidad-parking](#panel-vista-identidad-parking)                                                            | Panel de demo del Gemelo Digital - Pestaña parking                                  |
| Vista identidad: Transporte público                     | [gemelo-digital-vista-identidad-publictransport](#panel-vista-identidad-transporte-público)                                         | Panel de demo del Gemelo Digital - Pestaña Transporte público                       |
| Vista identidad: Tráfico                                | [gemelo-digital-vista-identidad-traffic](#panel-vista-identidad-tráfico)                                                            | Panel de demo del Gemelo Digital - Pestaña tráfico                                  |

## Descripción detallada de los paneles

### Panel: "Tablero de simulación: Corte de calle de larga duración"

- **Descripción**: Tablero de simulación del Gemelo Digital - Pestaña corte de calle de larga duración
- **Slug**: gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion
- **Idiomas disponibles**: Catalán, Ingles, Español
- **Enlaces**:

| Título                                                  | Panel                                                                                                                               | Eventos                                                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Tablero de simulación: Corte de calle de larga duración | [gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion](#panel-tablero-de-simulación-corte-de-calle-de-larga-duración) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nueva línea EMT                  | [gemelo-digital-tablero-simulacion-nueva-linea-emt](#panel-tablero-de-simulación-nueva-línea-emt)                                   | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nuevo parking                    | [gemelo-digital-tablero-simulacion-nuevo-parking](#panel-tablero-de-simulación-nuevo-parking)                                       | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Peatonalización de calle         | [gemelo-digital-tablero-simulacion-peatonalizacion-de-calle](#panel-tablero-de-simulación-peatonalización-de-calle)                 | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                               | Tipo         | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------ | ------------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [*Sin título*](#control-sin-título)                                                  | refresher    | control   | Actualizar datos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Tabs](#widget-tabs)                                                                 | tabs         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Tramos seleccionados](#widget-tramos-seleccionados)                                 | table        | widget    | Muestra el listado de los tramos de tráfico de Valencia. Por defecto, muestra el total de tramos. Si se activa el bounding box del mapa a la derecha, automáticamente se filtran los tramos y aparecerán listados únicamente los que estén incluidos en la visualización del mapa en ese momento.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [Localización de los tramos](#widget-localización-de-los-tramos)                     | basic-map-ol | widget    | En este mapa están representados por defecto todos los tramos de tráfico de Valencia. Para comenzar a registrar la simulación del corte de una calle de larga duración, debe hacerse zoom en el mapa hasta visualizar únicamente los tramos afectados por el corte (en el listado de los tramos a la izquierda aparecen desglosados) y a continuación se debe activar el bounding box de la esquina superior izquierda del mapa.                                                                                                                                                                                                                                                                                                    |
| [Nueva simulación](#widget-nueva-simulación)                                         | detail       | widget    | En este formulario se registran las características de la simulación del corte de una calle de larga duración. Para ello, previamente se ha debido seleccionar en el mapa (mediante el bounding box) los tramos afectados. A continuación, se deberán rellenar como mínimo los campos marcados como obligatorios en el formulario. Algunos campos requieren que su contenido respete ciertas reglas: el texto para la definición del id de la nueva simulación debe tener un formato alfanumérico y solo se permiten guiones y guiones bajos (se excluyen caracteres como -ñ-). Su extensión no debe superar los 30 caracteres. Ejemplo: Corte_5_Calle_San_Jacinto./ El valor del campo impacto debe estar comprendido entre 1 y 9. |
| [Uso del transporte público](#widget-uso-del-transporte-público)                     | iframe       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Listado de simulaciones realizadas](#widget-listado-de-simulaciones-realizadas)     | table        | widget    | Esta tabla muestra la lista de las simulaciones que han sido realizadas. Permite borrar simulaciones que no se desean mantener. En la columna -Estado- puede verse el estado de ejecución de la simulación (desde -new- hasta -done-). Sólo podrán visualizarse los datos de la simulación configurada una vez que haya terminado su ejecución y esté en -done-. Pulsando sobre la tabla se verán los detalles de configuración de la simulación seleccionada en los widgets de abajo                                                                                                                                                                                                                                               |
| [Detalles de la simulación](#widget-detalles-de-la-simulación)                       | detail       | widget    | Detalle de la simulación seleccionada en la tabla superior. Sólo para visualizar datos.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Localización de los tramos simulados](#widget-localización-de-los-tramos-simulados) | basic-map-ol | widget    | Localización en el mapa de los tramos afectados por la simulación seleccionada en la tabla superior. Si se hace click en un tramo concreto, se abre una ventana con el código del tramo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Tramos seleccionados](#widget-tramos-seleccionados-1)                               | table        | widget    | Muestra la lista de los tramos afectados por la simulación seleccionada en la tabla superior.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: Tramos seleccionados

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_FILTER | `ON_BBOX`     |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Localización de los tramos

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "sources": {
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot    | Id del evento |
| ------- | ------------- |
| ON_BBOX | `ON_BBOX`     |

- **Eventos recibidos**: Ninguno

#### Widget: Nueva simulación

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationTraffic",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento      |
| --------- | ------------------ |
| ON_RELOAD | `ON_RELOAD_DETAIL` |

- **Eventos recibidos**:

| Slot        | Id del evento                                                  |
| ----------- | -------------------------------------------------------------- |
| SET_CONTENT | `[{"fromEvent": "ON_BBOX", "mapping": {"location": "value"}}]` |
| SOURCE      | `[{"fromEvent": "ON_ROW_STOPS", "mapping": {"id": "id"}}]`     |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}smartbuildings_building_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Listado de simulaciones realizadas

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationTraffic",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_ROW    | `ON_ROW_SIMULATION_TABLE`    |

- **Eventos recibidos**:

| Slot      | Id del evento                       |
| --------- | ----------------------------------- |
| ON_RELOAD | `["ON_RELOAD", "ON_RELOAD_DETAIL"]` |

#### Widget: Detalles de la simulación

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationTraffic",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_RELOAD | `ON_RELOAD`                  |

#### Widget: Localización de los tramos simulados

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "sources": {
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_BBOX   | `[{"fromEvent": "ON_ROW_SIMULATION_TABLE", "mapping": {"value": "location|jsonparse"}, "stages": ["mapping", "static"], "static": {"operator": "intersect", "var": "location"}}]` |
| ON_RELOAD | `ON_RELOAD`                                                                                                                                                                       |

#### Widget: Tramos seleccionados

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"fromEvent": "ON_ROW_SIMULATION_TABLE", "mapping": {"value": "location|jsonparse"}, "stages": ["mapping", "static"], "static": {"operator": "intersect", "var": "location"}}]` |
| ON_RELOAD | `ON_RELOAD`                                                                                                                                                                       |

### Panel: "Tablero de simulación: Nueva línea EMT"

- **Descripción**: Tablero de simulación del Gemelo Digital - Pestaña nueva línea EMT
- **Slug**: gemelo-digital-tablero-simulacion-nueva-linea-emt
- **Idiomas disponibles**: Catalán, Ingles, Español
- **Enlaces**:

| Título                                                  | Panel                                                                                                                               | Eventos                                                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Tablero de simulación: Corte de calle de larga duración | [gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion](#panel-tablero-de-simulación-corte-de-calle-de-larga-duración) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nueva línea EMT                  | [gemelo-digital-tablero-simulacion-nueva-linea-emt](#panel-tablero-de-simulación-nueva-línea-emt)                                   | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nuevo parking                    | [gemelo-digital-tablero-simulacion-nuevo-parking](#panel-tablero-de-simulación-nuevo-parking)                                       | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Peatonalización de calle         | [gemelo-digital-tablero-simulacion-peatonalizacion-de-calle](#panel-tablero-de-simulación-peatonalización-de-calle)                 | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                             | Tipo         | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------- | ------------ | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [*Sin título*](#control-sin-título-1)                                              | refresher    | control   | Actualizar datos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Tabs](#widget-tabs-1)                                                             | tabs         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Nuevas paradas](#widget-nuevas-paradas)                                           | detail       | widget    | En este formulario se registran las paradas de la nueva línea EMT a simular. Para ello, previamente se ha debido pulsar en el mapa para indicar la posición de la parada. A continuación, se deberán rellenar como mínimo los campos marcados como obligatorios. Se irán añadiendo las paradas en la tabla de la derecha en orden secuencial a su creación. El recorrido de la nueva línea tendrá, por tanto, la resultante de unir las paradas según orden de creación.                                                                                                                                                                                                                                                                                                                                                   |
| [Seleccione paradas en el mapa](#widget-seleccione-paradas-en-el-mapa)             | basic-map-ol | widget    | Este mapa permite seleccionar la posición de las paradas para generar una nueva ruta simulada. Simplemente pulsando sobre él quedará definida la ubicación de la parada y se representará con un marcador de color verde. La posición será automáticamente introducida en el formulario de la izquierda // Por defecto, se representan las líneas reales de la EMT existentes en Valencia (a modo de referencia). Haciendo click sobre alguna de ellas, se abre una ventana con su nombre y el número de viajeros habituales.                                                                                                                                                                                                                                                                                              |
| [Paradas de la nueva línea](#widget-paradas-de-la-nueva-línea)                     | table        | widget    | Este widget muestra una lista de las paradas que se han ido añadiendo en el formulario de la izquierda conforme al procedimiento que se describe en aquel.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Nueva simulación](#widget-nueva-simulación-1)                                     | detail       | widget    | En este formulario se registran las características de la nueva línea a simular. Para ello, previamente se ha debido pulsar en el mapa para indicar las posiciones de las paradas que la conformarán. A continuación, se deberán rellenar como mínimo los campos marcados como obligatorios. Algunos campos requieren que su contenido respete ciertas reglas: en primer lugar, el texto para la definición del id de la nueva simulación debe tener un formato alfanumérico y solo se permiten guiones y guiones bajos (se excluyen caracteres como -ñ-). Su extensión no debe superar los 30 caracteres. Ejemplo: EMT_17_Circular. / Para los campos de número de trayectos y viajeros previstos, los valores deben ser entre 1 y 999999. / Y por último, el valor del campo impacto debe estar comprendido entre 1 y 9. |
| [Uso del transporte público](#widget-uso-del-transporte-público-1)                 | iframe       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Listado de simulaciones realizadas](#widget-listado-de-simulaciones-realizadas-1) | table        | widget    | Esta tabla muestra la lista de las simulaciones que han sido realizadas. Permite borrar simulaciones que no se desean mantener. En la columna -Estado- puede verse el estado de ejecución de la simulación (desde -new- hasta -done-). Sólo podrán visualizarse los datos de la simulación configurada una vez que haya terminado su ejecución y esté en -done-. Pulsando sobre la tabla se verán los detalles de configuración de la simulación seleccionada en los widgets de abajo.                                                                                                                                                                                                                                                                                                                                     |
| [Detalle de la simulación](#widget-detalle-de-la-simulación)                       | detail       | widget    | Detalle de la simulación seleccionada en la tabla superior. Sólo para visualizar datos.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Ruta simulada](#widget-ruta-simulada)                                             | basic-map-ol | widget    | Representación en el mapa de las líneas simuladas. Por defecto muestra todos las líneas simuladas que están listadas en la tabla superior. Si se selecciona una línea de entre las simulaciones, el mapa mostrará solamente esa línea.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: Nuevas paradas

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "Stop",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento     |
| --------- | ----------------- |
| ON_RELOAD | `ON_RELOAD_STOPS` |

- **Eventos recibidos**:

| Slot        | Id del evento                                                                   |
| ----------- | ------------------------------------------------------------------------------- |
| ON_RELOAD   | `ON_RELOAD`                                                                     |
| SET_CONTENT | `[{"fromEvent": "GEOJSON_STOPS", "mapping": {"location": "geojson.geometry"}}]` |
| SOURCE      | `[{"fromEvent": "ON_ROW_STOPS", "mapping": {"id": "id"}}]`                      |

#### Widget: Seleccione paradas en el mapa

- **Descripción**: Eventos
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de localizaci\u00f3n",
    "sources": {
        "cb-layer": {
            "connectionProperties": {
                "entityType": "Stop",
                "geomVar": "location",
                "subservice": "/gemelodigital"
            },
            "name": "@{dsName}",
            "type": "contextbroker"
        },
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot     | Id del evento   |
| -------- | --------------- |
| LOCATION | `GEOJSON_STOPS` |

- **Eventos recibidos**:

| Slot                | Id del evento                      |
| ------------------- | ---------------------------------- |
| GEOJSON_LAYER_STOPS | `GEOJSON_STOPS`                    |
| ON_BBOX             | `ON_BBOX_FROM_ROUTE_PLANNER`       |
| ON_RELOAD           | `["ON_RELOAD", "ON_RELOAD_STOPS"]` |
| ON_ROW_STOPS        | `ON_ROW_STOPS`                     |

#### Widget: Paradas de la nueva línea

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "Stop",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                      |
| --------- | ---------------------------------- |
| ON_RELOAD | `["ON_RELOAD", "ON_RELOAD_STOPS"]` |

#### Widget: Nueva simulación

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationRoute",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**: Ninguno

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}smartbuildings_building_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Listado de simulaciones realizadas

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationRoute",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_ROW    | `ON_ROW_SIMULATION_TABLE`    |

- **Eventos recibidos**:

| Slot      | Id del evento                       |
| --------- | ----------------------------------- |
| ON_RELOAD | `["ON_RELOAD", "ON_RELOAD_DETAIL"]` |

#### Widget: Detalle de la simulación

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationRoute",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_RELOAD | `ON_RELOAD`                  |

#### Widget: Ruta simulada

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "sources": {
        "simulation-location": {
            "connectionProperties": {
                "entityType": "SimulationRoute",
                "geomVar": "location",
                "subservice": "/gemelodigital"
            },
            "name": "@{dsName}",
            "type": "contextbroker"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_RELOAD | `ON_RELOAD`                  |

### Panel: "Tablero de simulación: Nuevo parking"

- **Descripción**: Tablero de simulación del Gemelo Digital - Pestaña nuevo parking
- **Slug**: gemelo-digital-tablero-simulacion-nuevo-parking
- **Idiomas disponibles**: Catalán, Ingles, Español
- **Enlaces**:

| Título                                                  | Panel                                                                                                                               | Eventos                                                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Tablero de simulación: Corte de calle de larga duración | [gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion](#panel-tablero-de-simulación-corte-de-calle-de-larga-duración) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nueva línea EMT                  | [gemelo-digital-tablero-simulacion-nueva-linea-emt](#panel-tablero-de-simulación-nueva-línea-emt)                                   | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nuevo parking                    | [gemelo-digital-tablero-simulacion-nuevo-parking](#panel-tablero-de-simulación-nuevo-parking)                                       | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Peatonalización de calle         | [gemelo-digital-tablero-simulacion-peatonalizacion-de-calle](#panel-tablero-de-simulación-peatonalización-de-calle)                 | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                             | Tipo         | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------------------- | ------------ | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [*Sin título*](#control-sin-título-2)                                              | refresher    | control   | Actualizar datos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Tabs](#widget-tabs-2)                                                             | tabs         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Nueva simulación](#widget-nueva-simulación-2)                                     | detail       | widget    | En este formulario se registran las características del nuevo parking a simular. Para ello, previamente se ha debido pulsar en el mapa para indicar la posición del parking. A continuación, se deberán rellenar como mínimo los campos marcados como obligatorios. Algunos campos requieren que su contenido respete ciertas reglas: el texto para la definición del id de la nueva simulación debe tener un formato alfanumérico y solo se permiten guiones y guiones bajos (se excluyen caracteres como -ñ-). Su extensión no debe superar los 30 caracteres. Ejemplo: Parking_14_La_Esperanza. / Para el campo capacidad de vehículos, los valores deben ser entre 1 y 99999. / Y por último, el valor del campo impacto debe estar comprendido entre 1 y 9. |
| [Seleccione posición en el mapa](#widget-seleccione-posición-en-el-mapa)           | basic-map-ol | widget    | Este mapa permite seleccionar la posición del nuevo parking a simular. Simplemente pulsando sobre él quedará definida la ubicación del parking y se representará con una P en el mapa. La posición será automáticamente introducida en el formulario de la izquierda // Con el símbolo de un punto de color magenta aparecen representados los parkings reales existentes en Valencia (a modo de referencia). Haciendo click sobre ellos, se abre una ventana con su nombre.                                                                                                                                                                                                                                                                                     |
| [Uso del transporte público](#widget-uso-del-transporte-público-2)                 | iframe       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Listado de simulaciones realizadas](#widget-listado-de-simulaciones-realizadas-2) | table        | widget    | Esta tabla muestra la lista de las simulaciones que han sido realizadas. Permite borrar simulaciones que no se desean mantener. En la columna -Estado- puede verse el estado de ejecución de la simulación (desde -new- hasta -done-). Sólo podrán visualizarse los datos de la simulación configurada una vez que haya terminado su ejecución y esté en -done-. Pulsando sobre la tabla se verán los detalles de configuración de la simulación seleccionada en los widgets de abajo.                                                                                                                                                                                                                                                                           |
| [Detalles de la simulación](#widget-detalles-de-la-simulación-1)                   | detail       | widget    | Detalle de la simulación seleccionada en la tabla superior. Sólo para visualizar datos.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [Posición del parking simulado](#widget-posición-del-parking-simulado)             | basic-map-ol | widget    | Detalle de la ubicación de los parkings simulados. Por defecto muestra todos los parkings simulados que están listados en la tabla superior. Si se selecciona un parking de la tabla superior, el mapa sólo muestra ese parking.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: Nueva simulación

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationParking",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento      |
| --------- | ------------------ |
| ON_RELOAD | `ON_RELOAD_DETAIL` |

- **Eventos recibidos**:

| Slot        | Id del evento                                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| SET_CONTENT | `[{"fromEvent": "GEOJSON_STOPS", "mapping": {"latitude": "lat", "location": "geojson.geometry", "longitude": "lon"}}]` |
| SOURCE      | `[{"fromEvent": "ON_ROW_STOPS", "mapping": {"id": "id"}}]`                                                             |

#### Widget: Seleccione posición en el mapa

- **Descripción**: Eventos
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito y de tipo de d\u00eda (laborable, s\u00e1bados, domingos). Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot     | Id del evento   |
| -------- | --------------- |
| LOCATION | `GEOJSON_STOPS` |

- **Eventos recibidos**:

| Slot                | Id del evento                |
| ------------------- | ---------------------------- |
| GEOJSON_LAYER_STOPS | `GEOJSON_STOPS`              |
| ON_BBOX             | `ON_BBOX_FROM_ROUTE_PLANNER` |
| ON_ROW_STOPS        | `ON_ROW_STOPS`               |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}smartbuildings_building_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Listado de simulaciones realizadas

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationParking",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_ROW    | `ON_ROW_SIMULATION_TABLE`    |

- **Eventos recibidos**:

| Slot      | Id del evento                       |
| --------- | ----------------------------------- |
| ON_RELOAD | `["ON_RELOAD", "ON_RELOAD_DETAIL"]` |

#### Widget: Detalles de la simulación

- **Descripción**:
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationParking",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_RELOAD | `ON_RELOAD`                  |

#### Widget: Posición del parking simulado

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "sources": {
        "simulation-location": {
            "connectionProperties": {
                "entityType": "SimulationParking",
                "geomVar": "location",
                "subservice": "/gemelodigital"
            },
            "name": "@{dsName}",
            "type": "contextbroker"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_RELOAD | `ON_RELOAD`                  |

### Panel: "Tablero de simulación: Peatonalización de calle"

- **Descripción**: Tablero de simulación del Gemelo Digital - Pestaña peatonalización de calle
- **Slug**: gemelo-digital-tablero-simulacion-peatonalizacion-de-calle
- **Idiomas disponibles**: Catalán, Ingles, Español
- **Enlaces**:

| Título                                                  | Panel                                                                                                                               | Eventos                                                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Tablero de simulación: Corte de calle de larga duración | [gemelo-digital-tablero-simulacion-corte-de-calle-de-larga-duracion](#panel-tablero-de-simulación-corte-de-calle-de-larga-duración) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nueva línea EMT                  | [gemelo-digital-tablero-simulacion-nueva-linea-emt](#panel-tablero-de-simulación-nueva-línea-emt)                                   | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Nuevo parking                    | [gemelo-digital-tablero-simulacion-nuevo-parking](#panel-tablero-de-simulación-nuevo-parking)                                       | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Tablero de simulación: Peatonalización de calle         | [gemelo-digital-tablero-simulacion-peatonalizacion-de-calle](#panel-tablero-de-simulación-peatonalización-de-calle)                 | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                 | Tipo         | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------- | ------------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [*Sin título*](#control-sin-título-3)                                                  | refresher    | control   | Actualizar datos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Tabs](#widget-tabs-3)                                                                 | tabs         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Tramos seleccionados](#widget-tramos-seleccionados-2)                                 | table        | widget    | Muestra el listado de los tramos de tráfico de Valencia. Por defecto, muestra el total de tramos. Si se activa el bounding box del mapa a la derecha, automáticamente se filtran los tramos y aparecerán listados únicamente los que estén incluidos en la visualización del mapa en ese momento.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [Localización de los tramos](#widget-localización-de-los-tramos-1)                     | basic-map-ol | widget    | En este mapa están representados por defecto todos los tramos de tráfico de Valencia. Para comenzar a registrar la simulación de la peatonalización de una calle, debe hacerse zoom en el mapa hasta visualizar únicamente los tramos a peatonalizar (en el listado de los tramos a la izquierda aparecen desglosados) y a continuación se debe activar el bounding box de la esquina superior izquierda del mapa.                                                                                                                                                                                                                                                                                                                  |
| [Nueva simulación](#widget-nueva-simulación-3)                                         | detail       | widget    | En este formulario se registran las características de la nueva simulación de peatonalización de una calle. Para ello, previamente se ha debido seleccionar en el mapa (mediante el bounding box) los tramos afectados. A continuación, se deberán rellenar como mínimo los campos marcados como obligatorios en el formulario. Algunos campos requieren que su contenido respete ciertas reglas: el texto para la definición del id de la nueva simulación debe tener un formato alfanumérico y solo se permiten guiones y guiones bajos (se excluyen caracteres como -ñ-). Su extensión no debe superar los 30 caracteres. Ejemplo: Peatonal_5_Calle_San_Jacinto./ El valor del campo impacto debe estar comprendido entre 1 y 9. |
| [Uso del transporte público](#widget-uso-del-transporte-público-3)                     | iframe       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Listado de simulaciones realizadas](#widget-listado-de-simulaciones-realizadas-3)     | table        | widget    | Esta tabla muestra la lista de las simulaciones que han sido realizadas. Permite borrar simulaciones que no se desean mantener. En la columna -Estado- puede verse el estado de ejecución de la simulación (desde -new- hasta -done-). Sólo podrán visualizarse los datos de la simulación configurada una vez que haya terminado su ejecución y esté en -done-. Pulsando sobre la tabla se verán los detalles de configuración de la simulación seleccionada en los widgets de abajo                                                                                                                                                                                                                                               |
| [Detalles de la simulación](#widget-detalles-de-la-simulación-2)                       | detail       | widget    | Detalle de la simulación seleccionada en la tabla superior. Sólo para visualizar datos.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Localización de los tramos simulados](#widget-localización-de-los-tramos-simulados-1) | basic-map-ol | widget    | Localización en el mapa de los tramos afectados por la simulación seleccionada en la tabla superior. Si se hace click en un tramo concreto, se abre una ventana con el código del tramo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Tramos seleccionados](#widget-tramos-seleccionados-3)                                 | table        | widget    | Muestra la lista de los tramos afectados por la simulación seleccionada en la tabla superior.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: Tramos seleccionados

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_FILTER | `ON_BBOX`     |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Localización de los tramos

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "sources": {
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot    | Id del evento |
| ------- | ------------- |
| ON_BBOX | `ON_BBOX`     |

- **Eventos recibidos**: Ninguno

#### Widget: Nueva simulación

- **Descripción**: Detalle de la entidad
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationTraffic",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento      |
| --------- | ------------------ |
| ON_RELOAD | `ON_RELOAD_DETAIL` |

- **Eventos recibidos**:

| Slot        | Id del evento                                                  |
| ----------- | -------------------------------------------------------------- |
| SET_CONTENT | `[{"fromEvent": "ON_BBOX", "mapping": {"location": "value"}}]` |
| SOURCE      | `[{"fromEvent": "ON_ROW_STOPS", "mapping": {"id": "id"}}]`     |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}smartbuildings_building_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Listado de simulaciones realizadas

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationTraffic",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_ROW    | `ON_ROW_SIMULATION_TABLE`    |

- **Eventos recibidos**:

| Slot      | Id del evento                       |
| --------- | ----------------------------------- |
| ON_RELOAD | `["ON_RELOAD", "ON_RELOAD_DETAIL"]` |

#### Widget: Detalles de la simulación

- **Descripción**:
- **Tipo**: detail
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "SimulationTraffic",
        "subservice": "/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                |
| --------- | ---------------------------- |
| ON_FILTER | `ON_FILTER_SIMULATION_TABLE` |
| ON_RELOAD | `ON_RELOAD`                  |

#### Widget: Localización de los tramos simulados

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "sources": {
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_BBOX   | `[{"fromEvent": "ON_ROW_SIMULATION_TABLE", "mapping": {"value": "location|jsonparse"}, "stages": ["mapping", "static"], "static": {"operator": "intersect", "var": "location"}}]` |
| ON_RELOAD | `ON_RELOAD`                                                                                                                                                                       |

#### Widget: Tramos seleccionados

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"fromEvent": "ON_ROW_SIMULATION_TABLE", "mapping": {"value": "location|jsonparse"}, "stages": ["mapping", "static"], "static": {"operator": "intersect", "var": "location"}}]` |
| ON_RELOAD | `ON_RELOAD`                                                                                                                                                                       |

### Panel: "Panel comparación"

- **Descripción**: Panel de demo del Gemelo Digital. Vista comparativa
- **Slug**: gemelo-digital-panel-comparacion
- **Idiomas disponibles**: Ingles, Español

El panel consta de los siguientes widgets:

| Título                                                                                                                                                    | Tipo           | Ubicación | Descripción                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------ |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title)                                         | selector       | control   |                                                                                |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title)                                         | selector       | control   |                                                                                |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title)                                         | selector       | control   |                                                                                |
| [*Sin título*](#control-sin-título-4)                                                                                                                     | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                     |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title)                                          | selector       | widget    |                                                                                |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title)                                              | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                       |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-1)                                            | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                       |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title-1)                                        | selector       | widget    |                                                                                |
| [ranking-parking_conf_title](#widget-ranking-parkingconftitle)                                                                                            | horizontal-bar | widget    | ranking-parking_conf_description                                               |
| [i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-parkingwidgets4conftitle)                   | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_description         |
| [i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-parkingwidgets4conftitle-1)                 | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_description         |
| [ranking-parking_conf_title](#widget-ranking-parkingconftitle-1)                                                                                          | horizontal-bar | widget    | ranking-parking_conf_description                                               |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets5conftitle)   | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_description |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets4conftitle)   | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_description |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets4conftitle-1) | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_description |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets5conftitle-1) | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_description |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets5conftitle)                   | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_description         |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets4conftitle)                   | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_description         |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets4conftitle-1)                 | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_description         |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets5conftitle-1)                 | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_description         |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                     |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF_LEFT"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "estado-esperado_description",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "estado-esperado_description",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF_RIGHT"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: ranking-parking_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_offstreetparking_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_offstreetparking_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

#### Widget: ranking-parking_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                               |
| --------- | ------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_LEFT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                 |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                |
| --------- | -------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF_RIGHT"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                  |

### Panel: "Vista identidad: Estado general"

- **Descripción**: Panel de demo del Gemelo Digital
- **Slug**: gemelo-digital-vista-identidad
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                              | Panel                                                                                       | Eventos                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista identidad: Urbanismo          | [gemelo-digital-vista-identidad-city](#panel-vista-identidad-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Estado general     | [gemelo-digital-vista-identidad](#panel-vista-identidad-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Parking            | [gemelo-digital-vista-identidad-parking](#panel-vista-identidad-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Transporte público | [gemelo-digital-vista-identidad-publictransport](#panel-vista-identidad-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Tráfico            | [gemelo-digital-vista-identidad-traffic](#panel-vista-identidad-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                                                                    | Tipo           | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Seleccione una temporada](#control-seleccione-una-temporada)                                                                                             | selector       | control   |                                                                                                                                                                                                                                                                                                                                                     |
| [Seleccione un distrito](#control-seleccione-un-distrito)                                                                                                 | selector       | control   |                                                                                                                                                                                                                                                                                                                                                     |
| [Seleccione un tipo de día](#control-seleccione-un-tipo-de-día)                                                                                           | selector       | control   |                                                                                                                                                                                                                                                                                                                                                     |
| [*Sin título*](#control-sin-título-5)                                                                                                                     | refresher      | control   | Actualizar datos                                                                                                                                                                                                                                                                                                                                    |
| [Tabs](#widget-tabs-4)                                                                                                                                    | tabs           | widget    |                                                                                                                                                                                                                                                                                                                                                     |
| [Estado esperado de los servicios](#widget-estado-esperado-de-los-servicios)                                                                              | basic-map-ol   | widget    | Mapa de Valencia con el estado esperado de los principales servicios: nivel de ocupación de los parkings, nivel de congestión del tráfico y utilización del transporte público. Se actualiza según los selectores de distrito, tipo de día (laborable, sábados, domingos) y temporada. Por defecto muestra el estado para el tipo de día laborable. |
| [Ocupación de los parkings](#widget-ocupación-de-los-parkings)                                                                                            | gauge          | widget    | Nivel medio de ocupación de los parkings de Valencia. Muestra información de un único parking si ha sido seleccionado en el mapa y se actualiza con los selectores de distrito, tipo de día y temporada.                                                                                                                                            |
| [Estado EMT](#widget-estado-emt)                                                                                                                          | gauge          | widget    | Nivel medio del uso del transporte público de Valencia, representado a través del número total de viajeros para el tipo de día por defecto (laborable) para todas las líneas. Se actualiza según los selectores de distrito, tipo de día y temporada.                                                                                               |
| [Estado del tráfico](#widget-estado-del-tráfico)                                                                                                          | gauge          | widget    | Nivel medio de congestión del tráfico en las vías de circulación de la ciudad de Valencia. Muestra información de un único tramo si ha sido seleccionado en el mapa y se actualiza según los selectores de distrito, tipo de día y temporada.                                                                                                       |
| [i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-parkingwidgets4conftitle-2)                 | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_description                                                                                                                                                                                                                                                                              |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets4conftitle-2) | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_description                                                                                                                                                                                                                                                                      |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets4conftitle-2)                 | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_description                                                                                                                                                                                                                                                                              |
| [i18n_gemelo-digital-vista-identidad-parking_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-parkingwidgets5conftitle)                   | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-parking_widgets_5_conf_description                                                                                                                                                                                                                                                                              |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets5conftitle-2) | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_description                                                                                                                                                                                                                                                                      |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets5conftitle-2)                 | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_description                                                                                                                                                                                                                                                                              |
| [i18n_gemelo-digital-vista-identidad-city_widgets_8_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets8conftitle)                         | table          | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_8_conf_description                                                                                                                                                                                                                                                                                 |
| [i18n_gemelo-digital-vista-identidad-city_widgets_9_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets9conftitle)                         | sloted-data    | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_9_conf_description                                                                                                                                                                                                                                                                                 |
| [i18n_gemelo-digital-vista-identidad-city_widgets_10_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets10conftitle)                       | sloted-data    | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_10_conf_description                                                                                                                                                                                                                                                                                |
| [i18n_gemelo-digital-vista-identidad-city_widgets_11_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets11conftitle)                       | sloted-data    | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_11_conf_description                                                                                                                                                                                                                                                                                |

#### Control: Seleccione una temporada

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: Seleccione un distrito

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: Seleccione un tipo de día

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: Estado esperado de los servicios

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "estado-esperado_description",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Ocupación de los parkings

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Estado EMT

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Estado del tráfico

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_offstreetparking_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-parking_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_8_conf_title

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_airqualityobserved_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_9_conf_title

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_10_conf_title

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_11_conf_title

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

### Panel: "Vista simulada: Urbanismo"

- **Descripción**: Panel de demo del Gemelo Digital. Vista simulada. Pestaña urbanismo.
- **Slug**: gemelo-digital-vista-simulada-city
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                             | Panel                                                                                     | Eventos                                                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista simulada: Urbanismo          | [gemelo-digital-vista-simulada-city](#panel-vista-simulada-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Estado general     | [gemelo-digital-vista-simulada](#panel-vista-simulada-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Transporte público | [gemelo-digital-vista-simulada-publictransport](#panel-vista-simulada-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Tráfico            | [gemelo-digital-vista-simulada-traffic](#panel-vista-simulada-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                              | Tipo         | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------- | ------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-1) | selector     | control   |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-1) | selector     | control   |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-1) | selector     | control   |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [*Sin título*](#control-sin-título-6)                                                                               | refresher    | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                                                                                                                                                                                                       |
| [Tabs](#widget-tabs-5)                                                                                              | tabs         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title-2)  | selector     | widget    |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-2)      | basic-map-ol | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                                                                                                                                                                                         |
| [](#widget-)                                                                                                        | iframe       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Calidad del aire por distrito](#widget-calidad-del-aire-por-distrito)                                              | table        | widget    | Valores de los principales indicadores de calidad del aire para los diferentes distritos de Valencia                                                                                                                                                                                                                                                                                             |
| [Presupuesto anual](#widget-presupuesto-anual)                                                                      | sloted-data  | widget    | Presupuesto anual de Valencia para el último año modelado.                                                                                                                                                                                                                                                                                                                                       |
| [IBI medio](#widget-ibi-medio)                                                                                      | sloted-data  | widget    | Impuesto Sobre Bienes Inmuebles medio de Valencia para el último año modelado.                                                                                                                                                                                                                                                                                                                   |
| [Inflación](#widget-inflación)                                                                                      | sloted-data  | widget    | Valor de la inflación para el último año modelado.                                                                                                                                                                                                                                                                                                                                               |
| [Tasa de desempleo](#widget-tasa-de-desempleo)                                                                      | sloted-data  | widget    | Porcentaje que representa el número total de desempleados con respecto a la población activa para Valencia para el último año modelado.                                                                                                                                                                                                                                                          |
| [Titulados Superiores](#widget-titulados-superiores)                                                                | sloted-data  | widget    | Número de titulados de educación superior por cada 100.000 habitantes para Valencia para el último año modelado.                                                                                                                                                                                                                                                                                 |
| [Densidad residencial](#widget-densidad-residencial)                                                                | sloted-data  | widget    | Cociente entre el número de personas del año de referencia y la superficie de la ciudad de Valencia, excepto la superficie del puerto y del lago de la Albufera. Representa el número medio de personas por kilómetro cuadrado de la superficie potencialmente habitable de la ciudad.                                                                                                           |
| [Zonas verdes](#widget-zonas-verdes)                                                                                | sloted-data  | widget    | Zonas verdes de acceso público por 100 000 habitantes. Dentro de los espacios verdes están incluidos parques, jardines, áreas recreativas, zonas naturales u otros espacios verdes abiertos. Se calcula como el área total de los espacios verdes en la ciudad (numerador), dividido por 1 cada 100.000 habitantes (denominador). El resultado será expresado como hectáreas/100.000 habitantes. |
| [Superficie urbana](#widget-superficie-urbana)                                                                      | sloted-data  | widget    | Superficie del Municipio para el último año modelado. Observaciones: La superficie proviene del cálculo del área definida por los límites municipales registrada en el SIGESPA. Pueden observarse variaciones anuales debido a modificaciones en la superficie del Puerto de Valencia o a correcciones en los límites municipales de la ciudad.                                                  |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito y de tipo de d\u00eda (laborable, s\u00e1bados, domingos). Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: 

- **Descripción**: Nivel medio de congestión del tráfico, en las vías de circulación de la ciudad de Valencia. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Calidad del aire por distrito

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_airqualityobserved_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_SCENEREF", "ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: Presupuesto anual

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: IBI medio

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Inflación

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Tasa de desempleo

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Titulados Superiores

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Densidad residencial

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Zonas verdes

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Superficie urbana

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

### Panel: "Vista simulada: Estado general"

- **Descripción**: Panel de demo del Gemelo Digital. Vista simulada
- **Slug**: gemelo-digital-vista-simulada
- **Idiomas disponibles**: Ingles, Español, Valenciano
- **Enlaces**:

| Título                             | Panel                                                                                     | Eventos                                                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista simulada: Urbanismo          | [gemelo-digital-vista-simulada-city](#panel-vista-simulada-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Estado general     | [gemelo-digital-vista-simulada](#panel-vista-simulada-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Parking            | [gemelo-digital-vista-simulada-parking](#panel-vista-simulada-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Transporte público | [gemelo-digital-vista-simulada-publictransport](#panel-vista-simulada-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Tráfico            | [gemelo-digital-vista-simulada-traffic](#panel-vista-simulada-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                                                                    | Tipo           | Ubicación | Descripción                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------ |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-2)                                       | selector       | control   |                                                                                |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-2)                                       | selector       | control   |                                                                                |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-2)                                       | selector       | control   |                                                                                |
| [*Sin título*](#control-sin-título-7)                                                                                                                     | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                     |
| [i18n_gemelo-digital-vista-identidad_widgets_0_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets0conftitle)                                   | tabs           | widget    |                                                                                |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title-3)                                        | selector       | widget    |                                                                                |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-3)                                            | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                       |
| [i18n_gemelo-digital-vista-identidad_widget_3_title](#widget-i18ngemelo-digital-vista-identidadwidget3title)                                              | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widget_3_description                       |
| [i18n_gemelo-digital-vista-identidad_widgets_3_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets3conftitle)                                   | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widgets_3_conf_description                 |
| [i18n_gemelo-digital-vista-identidad_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets4conftitle)                                   | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widgets_4_conf_description                 |
| [i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-parkingwidgets4conftitle-3)                 | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_description         |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets4conftitle-3) | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_description |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets4conftitle-3)                 | timeseries     | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_description         |
| [i18n_gemelo-digital-vista-identidad-parking_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-parkingwidgets5conftitle-1)                 | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-parking_widgets_5_conf_description         |
| [i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-publictransportwidgets5conftitle-3) | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_description |
| [i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title](#widget-i18ngemelo-digital-vista-identidad-trafficwidgets5conftitle-3)                 | horizontal-bar | widget    | i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_description         |
| [i18n_gemelo-digital-vista-identidad-city_widgets_8_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets8conftitle-1)                       | table          | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_8_conf_description            |
| [i18n_gemelo-digital-vista-identidad-city_widgets_9_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets9conftitle-1)                       | sloted-data    | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_9_conf_description            |
| [i18n_gemelo-digital-vista-identidad-city_widgets_10_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets10conftitle-1)                     | sloted-data    | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_10_conf_description           |
| [i18n_gemelo-digital-vista-identidad-city_widgets_11_conf_title](#widget-i18ngemelo-digital-vista-identidad-citywidgets11conftitle-1)                     | sloted-data    | widget    | i18n_gemelo-digital-vista-identidad-city_widgets_11_conf_description           |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_0_conf_title

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                           |
| --------- | ----------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE", "ON_FILTER_ESCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                             |

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "estado-esperado_description",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_3_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_3_conf_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_4_conf_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-parking_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_offstreetparking_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_4_conf_title

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-parking_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-publictransport_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-traffic_widgets_5_conf_title

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_8_conf_title

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_airqualityobserved_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_9_conf_title

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_10_conf_title

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad-city_widgets_11_conf_title

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

### Panel: "Vista simulada: Parking"

- **Descripción**: Panel de demo del Gemelo Digital. Vista simulada. Pestaña parking.
- **Slug**: gemelo-digital-vista-simulada-parking
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                             | Panel                                                                                     | Eventos                                                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista simulada: Urbanismo          | [gemelo-digital-vista-simulada-city](#panel-vista-simulada-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Estado general     | [gemelo-digital-vista-simulada](#panel-vista-simulada-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Parking            | [gemelo-digital-vista-simulada-parking](#panel-vista-simulada-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Transporte público | [gemelo-digital-vista-simulada-publictransport](#panel-vista-simulada-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Tráfico            | [gemelo-digital-vista-simulada-traffic](#panel-vista-simulada-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                              | Tipo           | Ubicación | Descripción                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-3) | selector       | control   |                                                                                                                                                                                                                                                                           |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-3) | selector       | control   |                                                                                                                                                                                                                                                                           |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-3) | selector       | control   |                                                                                                                                                                                                                                                                           |
| [*Sin título*](#control-sin-título-8)                                                                               | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                                                                                |
| [Tabs](#widget-tabs-6)                                                                                              | tabs           | widget    |                                                                                                                                                                                                                                                                           |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title-4)  | selector       | widget    |                                                                                                                                                                                                                                                                           |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-4)      | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                                                                  |
| [Uso del transporte público](#widget-uso-del-transporte-público-4)                                                  | iframe         | widget    |                                                                                                                                                                                                                                                                           |
| [i18n_gemelo-digital-vista-identidad_widget_3_title](#widget-i18ngemelo-digital-vista-identidadwidget3title-1)      | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widget_3_description                                                                                                                                                                                                                  |
| [Ocupación de los parkings por horas](#widget-ocupación-de-los-parkings-por-horas)                                  | timeseries     | widget    | Distribución de la ocupación de los parkings según las horas del día. Se actualiza con los selectores de distrito y de tipo de día                                                                                                                                        |
| [Ranking de parkings por ocupación](#widget-ranking-de-parkings-por-ocupación)                                      | horizontal-bar | widget    | Ranking de los parkings con doble ordenación según el valor medio de la ocupación diaria: de más a menos saturados y de menos a más saturados.                                                                                                                            |
| [Distribución de la ocupación de los parkings](#widget-distribución-de-la-ocupación-de-los-parkings)                | pie            | widget    | Muestra cómo se distribuye la ocupación del parking en el tiempo en el sentido de demanda plana vs picos de demanda. Muestra qué porcentaje del día el parking está en máxima ocupación y cuánto en mínima. Se actualiza con los selectores de distrito y de tipo de día. |
| [Horas pico y valle de los parkings](#widget-horas-pico-y-valle-de-los-parkings)                                    | table          | widget    | Detalle de horas pico y horas valle para todos los parkings, con dos franjas diarias (mañana y tarde). Se actualiza con el selector de de tipo de día.                                                                                                                    |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito y de tipo de d\u00eda (laborable, s\u00e1bados, domingos). Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_3_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Ocupación de los parkings por horas

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_offstreetparking_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Ranking de parkings por ocupación

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Distribución de la ocupación de los parkings

- **Descripción**:
- **Tipo**: pie
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_freq"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Horas pico y valle de los parkings

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_peak"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

### Panel: "Vista simulada: Transporte público"

- **Descripción**: Panel de demo del Gemelo Digital. Vista simulada. Pestaña transporte público
- **Slug**: gemelo-digital-vista-simulada-publictransport
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                             | Panel                                                                                     | Eventos                                                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista simulada: Urbanismo          | [gemelo-digital-vista-simulada-city](#panel-vista-simulada-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Estado general     | [gemelo-digital-vista-simulada](#panel-vista-simulada-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Parking            | [gemelo-digital-vista-simulada-parking](#panel-vista-simulada-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Transporte público | [gemelo-digital-vista-simulada-publictransport](#panel-vista-simulada-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Tráfico            | [gemelo-digital-vista-simulada-traffic](#panel-vista-simulada-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                                    | Tipo           | Ubicación | Descripción                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-4)       | selector       | control   |                                                                                                                                                                                                               |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-4)       | selector       | control   |                                                                                                                                                                                                               |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-4)       | selector       | control   |                                                                                                                                                                                                               |
| [*Sin título*](#control-sin-título-9)                                                                                     | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                    |
| [Tabs](#widget-tabs-7)                                                                                                    | tabs           | widget    |                                                                                                                                                                                                               |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title-5)        | selector       | widget    |                                                                                                                                                                                                               |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-5)            | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                      |
| [Uso del transporte público](#widget-uso-del-transporte-público-5)                                                        | iframe         | widget    |                                                                                                                                                                                                               |
| [i18n_gemelo-digital-vista-identidad_widgets_3_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets3conftitle-1) | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widgets_3_conf_description                                                                                                                                                |
| [Trayectos EMT por horas](#widget-trayectos-emt-por-horas)                                                                | timeseries     | widget    | Número de trayectos de las diferentes líneas, distribuidos según las horas del día en las que se efectúan. Se actualiza según los selectores de distrito y tipo de día.                                       |
| [Ranking de líneas por viajeros](#widget-ranking-de-líneas-por-viajeros)                                                  | horizontal-bar | widget    | Ranking de las líneas de la EMT con doble ordenación según el número de viajeros de cada una de ellas: de más a menos viajeros y de menos a más. Se actualiza según los selectores de distrito y tipo de día. |
| [Líneas por viajeros/trayecto/parada](#widget-líneas-por-viajerostrayectoparada)                                          | horizontal-bar | widget    | Comparación entre líneas del número medio de viajeros únicamente por trayecto, y también por trayecto y por parada. Se actualiza según los selectores de distrito y tipo de día.                              |
| [Horas pico y valle EMT](#widget-horas-pico-y-valle-emt)                                                                  | table          | widget    | Detalle de horas pico y horas valle para todas las líneas de la EMT, con dos franjas diarias (mañana y tarde). Se actualiza con los selectores de distrito y de tipo de día.                                  |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito y de tipo de d\u00eda (laborable, s\u00e1bados, domingos). Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_3_conf_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Trayectos EMT por horas

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Ranking de líneas por viajeros

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Líneas por viajeros/trayecto/parada

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_calc"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Horas pico y valle EMT

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_peak"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

### Panel: "Vista simulada: Tráfico"

- **Descripción**: Panel de demo del Gemelo Digital. Vista simulada. Pestaña tráfico
- **Slug**: gemelo-digital-vista-simulada-traffic
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                             | Panel                                                                                     | Eventos                                                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista simulada: Urbanismo          | [gemelo-digital-vista-simulada-city](#panel-vista-simulada-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Estado general     | [gemelo-digital-vista-simulada](#panel-vista-simulada-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Parking            | [gemelo-digital-vista-simulada-parking](#panel-vista-simulada-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Transporte público | [gemelo-digital-vista-simulada-publictransport](#panel-vista-simulada-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista simulada: Tráfico            | [gemelo-digital-vista-simulada-traffic](#panel-vista-simulada-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                                    | Tipo           | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-5)       | selector       | control   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-5)       | selector       | control   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-5)       | selector       | control   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [*Sin título*](#control-sin-título-10)                                                                                    | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                                                                                                                                                                                                              |
| [Tabs](#widget-tabs-8)                                                                                                    | tabs           | widget    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#widget-i18ngemelo-digital-vista-identidadselector3title-6)        | selector       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-6)            | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                                                                                                                                                                                                |
| [](#widget--1)                                                                                                            | iframe         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets4conftitle-1) | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widgets_4_conf_description                                                                                                                                                                                                                                                                                                                                          |
| [Congestión del tráfico por horas](#widget-congestión-del-tráfico-por-horas)                                              | timeseries     | widget    | Distribución de la congestión del tráfico según las horas del día. Se actualiza según los selectores de distrito y tipo de día                                                                                                                                                                                                                                                                          |
| [Ranking de tramos por congestión](#widget-ranking-de-tramos-por-congestión)                                              | horizontal-bar | widget    | Ranking de los tramos con doble ordenación según su congestión (valor medio diario): de más a menos congestionados y de menos a más. Se actualiza según los selectores de distrito y tipo de día.                                                                                                                                                                                                       |
| [IMD por distrito](#widget-imd-por-distrito)                                                                              | table          | widget    | Tabla con la intensidad media diaria (IMD) de los 19 distritos de Valencia. Para cada distrito, se muestra la IMD para el tipo de día por defecto (laborable). Se escoge el punto de medida con la IMD más alta. La IMD se obtiene sumando el total de vehículos que transitan por ese punto a lo largo de un año y dividiendo la suma entre los 365 días. Se actualiza con el selector de tipo de día. |
| [Horas pico y valle de tráfico](#widget-horas-pico-y-valle-de-tráfico)                                                    | table          | widget    | Detalle de horas pico (mayor probabilidad de congestión) y horas valle (menor probabilidad de congestión) para todos los tramos, con dos franjas diarias (mañana y tarde). Se actualiza con el selector de tipo de día.                                                                                                                                                                                 |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_simulation_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "sceneref"}, "toEvent": "ON_FILTER_SCENEREF"}]` |

- **Eventos recibidos**: Ninguno

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito y de tipo de d\u00eda (laborable, s\u00e1bados, domingos). Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: 

- **Descripción**: Nivel medio de congestión del tráfico, en las vías de circulación de la ciudad de Valencia. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_4_conf_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Congestión del tráfico por horas

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: Ranking de tramos por congestión

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

#### Widget: IMD por distrito

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_trafficintensity_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                          |
| --------- | -------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF"]` |
| ON_RELOAD | `ON_RELOAD`                                                                            |

#### Widget: Horas pico y valle de tráfico

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_peak"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_SCENEREF", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                                             |

### Panel: "Vista identidad: Urbanismo"

- **Descripción**: Panel de demo del Gemelo Digital - Pestaña Urbanismo
- **Slug**: gemelo-digital-vista-identidad-city
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                              | Panel                                                                                       | Eventos                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista identidad: Urbanismo          | [gemelo-digital-vista-identidad-city](#panel-vista-identidad-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Estado general     | [gemelo-digital-vista-identidad](#panel-vista-identidad-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Parking            | [gemelo-digital-vista-identidad-parking](#panel-vista-identidad-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Transporte público | [gemelo-digital-vista-identidad-publictransport](#panel-vista-identidad-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Tráfico            | [gemelo-digital-vista-identidad-traffic](#panel-vista-identidad-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                              | Tipo         | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------- | ------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-6) | selector     | control   |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-6) | selector     | control   |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-6) | selector     | control   |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [*Sin título*](#control-sin-título-11)                                                                              | refresher    | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                                                                                                                                                                                                       |
| [Tabs](#widget-tabs-9)                                                                                              | tabs         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-7)      | basic-map-ol | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                                                                                                                                                                                         |
| [](#widget--2)                                                                                                      | iframe       | widget    |                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Calidad del aire por distrito](#widget-calidad-del-aire-por-distrito-1)                                            | table        | widget    | Valores de los principales indicadores de calidad del aire para los diferentes distritos de Valencia. Se actualiza con los selectores de distrito, tipo de día y temporada                                                                                                                                                                                                                       |
| [Presupuesto anual](#widget-presupuesto-anual-1)                                                                    | sloted-data  | widget    | Presupuesto anual de Valencia para el último año modelado.                                                                                                                                                                                                                                                                                                                                       |
| [IBI medio](#widget-ibi-medio-1)                                                                                    | sloted-data  | widget    | Impuesto Sobre Bienes Inmuebles medio de Valencia para el último año modelado.                                                                                                                                                                                                                                                                                                                   |
| [Inflación](#widget-inflación-1)                                                                                    | sloted-data  | widget    | Valor de la inflación para el último año modelado.                                                                                                                                                                                                                                                                                                                                               |
| [Tasa de desempleo](#widget-tasa-de-desempleo-1)                                                                    | sloted-data  | widget    | Porcentaje que representa el número total de desempleados con respecto a la población activa para Valencia para el último año modelado.                                                                                                                                                                                                                                                          |
| [Titulados Superiores](#widget-titulados-superiores-1)                                                              | sloted-data  | widget    | Número de titulados de educación superior por cada 100.000 habitantes para Valencia para el último año modelado.                                                                                                                                                                                                                                                                                 |
| [Densidad residencial](#widget-densidad-residencial-1)                                                              | sloted-data  | widget    | Cociente entre el número de personas del año de referencia y la superficie de la ciudad de Valencia, excepto la superficie del puerto y del lago de la Albufera. Representa el número medio de personas por kilómetro cuadrado de la superficie potencialmente habitable de la ciudad.                                                                                                           |
| [Zonas verdes](#widget-zonas-verdes-1)                                                                              | sloted-data  | widget    | Zonas verdes de acceso público por 100 000 habitantes. Dentro de los espacios verdes están incluidos parques, jardines, áreas recreativas, zonas naturales u otros espacios verdes abiertos. Se calcula como el área total de los espacios verdes en la ciudad (numerador), dividido por 1 cada 100.000 habitantes (denominador). El resultado será expresado como hectáreas/100.000 habitantes. |
| [Superficie urbana](#widget-superficie-urbana-1)                                                                    | sloted-data  | widget    | Superficie del Municipio para el último año modelado. Observaciones: La superficie proviene del cálculo del área definida por los límites municipales registrada en el SIGESPA. Pueden observarse variaciones anuales debido a modificaciones en la superficie del Puerto de Valencia o a correcciones en los límites municipales de la ciudad.                                                  |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito y de tipo de d\u00eda (laborable, s\u00e1bados, domingos). Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: 

- **Descripción**: Nivel medio de congestión del tráfico, en las vías de circulación de la ciudad de Valencia. Se actualiza con los selectores de distrito y de tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Calidad del aire por distrito

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_airqualityobserved_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Presupuesto anual

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: IBI medio

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Inflación

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Tasa de desempleo

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Titulados Superiores

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Densidad residencial

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Zonas verdes

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: Superficie urbana

- **Descripción**:
- **Tipo**: sloted-data
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "entityType": "CityMetrics",
        "subservice": "@{subserviceRoot}/gemelodigital"
    },
    "type": "contextbroker"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

### Panel: "Vista identidad: Parking"

- **Descripción**: Panel de demo del Gemelo Digital - Pestaña parking
- **Slug**: gemelo-digital-vista-identidad-parking
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                              | Panel                                                                                       | Eventos                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista identidad: Urbanismo          | [gemelo-digital-vista-identidad-city](#panel-vista-identidad-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Estado general     | [gemelo-digital-vista-identidad](#panel-vista-identidad-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Parking            | [gemelo-digital-vista-identidad-parking](#panel-vista-identidad-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Transporte público | [gemelo-digital-vista-identidad-publictransport](#panel-vista-identidad-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Tráfico            | [gemelo-digital-vista-identidad-traffic](#panel-vista-identidad-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                              | Tipo           | Ubicación | Descripción                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-7) | selector       | control   |                                                                                                                                                                                                                                                                                   |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-7) | selector       | control   |                                                                                                                                                                                                                                                                                   |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-7) | selector       | control   |                                                                                                                                                                                                                                                                                   |
| [*Sin título*](#control-sin-título-12)                                                                              | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                                                                                        |
| [Tabs](#widget-tabs-10)                                                                                             | tabs           | widget    |                                                                                                                                                                                                                                                                                   |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-8)      | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                                                                          |
| [Uso del transporte público](#widget-uso-del-transporte-público-6)                                                  | iframe         | widget    |                                                                                                                                                                                                                                                                                   |
| [i18n_gemelo-digital-vista-identidad_widget_3_title](#widget-i18ngemelo-digital-vista-identidadwidget3title-2)      | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widget_3_description                                                                                                                                                                                                                          |
| [Ocupación de los parkings por horas](#widget-ocupación-de-los-parkings-por-horas-1)                                | timeseries     | widget    | Distribución de la ocupación de los parkings según las horas del día. Se actualiza con los selectores de distrito, tipo de día y temporada                                                                                                                                        |
| [Ranking de parkings por ocupación](#widget-ranking-de-parkings-por-ocupación-1)                                    | horizontal-bar | widget    | Ranking de los parkings con doble ordenación según el valor medio de la ocupación diaria: de más a menos saturados y de menos a más saturados.                                                                                                                                    |
| [Distribución de la ocupación de los parkings](#widget-distribución-de-la-ocupación-de-los-parkings-1)              | pie            | widget    | Muestra cómo se distribuye la ocupación del parking en el tiempo en el sentido de demanda plana vs picos de demanda. Muestra qué porcentaje del día el parking está en máxima ocupación y cuánto en mínima. Se actualiza con los selectores de distrito, tipo de día y temporada. |
| [Horas pico y valle de los parkings](#widget-horas-pico-y-valle-de-los-parkings-1)                                  | table          | widget    | Detalle de horas pico y horas valle para todos los parkings, con dos franjas diarias (mañana y tarde). Se actualiza con los selectores de distrito, tipo de día y temporada.                                                                                                      |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito, tipo de d\u00eda (laborable, s\u00e1bados, domingos) y temporada. Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito, temporada y tipo de día.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_3_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Ocupación de los parkings por horas

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_offstreetparking_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Ranking de parkings por ocupación

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Distribución de la ocupación de los parkings

- **Descripción**:
- **Tipo**: pie
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_freq"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Horas pico y valle de los parkings

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_offstreetparking_peak"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_MAP", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

### Panel: "Vista identidad: Transporte público"

- **Descripción**: Panel de demo del Gemelo Digital - Pestaña Transporte público
- **Slug**: gemelo-digital-vista-identidad-publictransport
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                              | Panel                                                                                       | Eventos                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista identidad: Urbanismo          | [gemelo-digital-vista-identidad-city](#panel-vista-identidad-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Estado general     | [gemelo-digital-vista-identidad](#panel-vista-identidad-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Parking            | [gemelo-digital-vista-identidad-parking](#panel-vista-identidad-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Transporte público | [gemelo-digital-vista-identidad-publictransport](#panel-vista-identidad-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Tráfico            | [gemelo-digital-vista-identidad-traffic](#panel-vista-identidad-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                                    | Tipo           | Ubicación | Descripción                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-8)       | selector       | control   |                                                                                                                                                                                                                          |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-8)       | selector       | control   |                                                                                                                                                                                                                          |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-8)       | selector       | control   |                                                                                                                                                                                                                          |
| [*Sin título*](#control-sin-título-13)                                                                                    | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                               |
| [Tabs](#widget-tabs-11)                                                                                                   | tabs           | widget    |                                                                                                                                                                                                                          |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-9)            | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                 |
| [Uso del transporte público](#widget-uso-del-transporte-público-7)                                                        | iframe         | widget    |                                                                                                                                                                                                                          |
| [i18n_gemelo-digital-vista-identidad_widgets_3_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets3conftitle-2) | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widgets_3_conf_description                                                                                                                                                           |
| [Trayectos EMT por horas](#widget-trayectos-emt-por-horas-1)                                                              | timeseries     | widget    | Número de trayectos de las diferentes líneas, distribuidos según las horas del día en las que se efectúan. Se actualiza según los selectores de distrito, tipo de día y temporada.                                       |
| [Ranking de líneas por viajeros](#widget-ranking-de-líneas-por-viajeros-1)                                                | horizontal-bar | widget    | Ranking de las líneas de la EMT con doble ordenación según el número de viajeros de cada una de ellas: de más a menos viajeros y de menos a más. Se actualiza según los selectores de distrito, tipo de día y temporada. |
| [Líneas por viajeros/trayecto/parada](#widget-líneas-por-viajerostrayectoparada-1)                                        | horizontal-bar | widget    | Comparación entre líneas del número medio de viajeros únicamente por trayecto, y también por trayecto y por parada. Se actualiza según los selectores de distrito, tipo de día y temporada.                              |
| [Horas pico y valle EMT](#widget-horas-pico-y-valle-emt-1)                                                                | table          | widget    | Detalle de horas pico y horas valle para todas las líneas de la EMT, con dos franjas diarias (mañana y tarde). Se actualiza con los selectores de distrito, tipo de día y temporada.                                     |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito, tipo de d\u00eda (laborable, s\u00e1bados, domingos) y temporada. Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Uso del transporte público

- **Descripción**: Nivel uso del transporte público de Valencia, según el número de trayectos de las diferentes líneas de la EMT. Se actualiza con los selectores de distrito, tipo de día y temporada.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_3_conf_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Trayectos EMT por horas

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Ranking de líneas por viajeros

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_sim"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Líneas por viajeros/trayecto/parada

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeintensity_calc"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Horas pico y valle EMT

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_routeschedule_peak"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

### Panel: "Vista identidad: Tráfico"

- **Descripción**: Panel de demo del Gemelo Digital - Pestaña tráfico
- **Slug**: gemelo-digital-vista-identidad-traffic
- **Idiomas disponibles**: Ingles, Español
- **Enlaces**:

| Título                              | Panel                                                                                       | Eventos                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Vista identidad: Urbanismo          | [gemelo-digital-vista-identidad-city](#panel-vista-identidad-urbanismo)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Estado general     | [gemelo-digital-vista-identidad](#panel-vista-identidad-estado-general)                     | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Parking            | [gemelo-digital-vista-identidad-parking](#panel-vista-identidad-parking)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Transporte público | [gemelo-digital-vista-identidad-publictransport](#panel-vista-identidad-transporte-público) | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |
| Vista identidad: Tráfico            | [gemelo-digital-vista-identidad-traffic](#panel-vista-identidad-tráfico)                    | `{"ON_FILTER_ENTITYID": "ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE": "ON_FILTER_ENTITYTYPE", "ON_FILTER_POI": "ON_FILTER_POI"}` |

El panel consta de los siguientes widgets:

| Título                                                                                                                    | Tipo           | Ubicación | Descripción                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [i18n_gemelo-digital-vista-identidad_selector_3_title](#control-i18ngemelo-digital-vista-identidadselector3title-9)       | selector       | control   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_selector_1_title](#control-i18ngemelo-digital-vista-identidadselector1title-9)       | selector       | control   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_selector_2_title](#control-i18ngemelo-digital-vista-identidadselector2title-9)       | selector       | control   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [*Sin título*](#control-sin-título-14)                                                                                    | refresher      | control   | i18n_gemelo-digital-vista-identidad_selector_3_description                                                                                                                                                                                                                                                                                                                                              |
| [Tabs](#widget-tabs-12)                                                                                                   | tabs           | widget    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_widget_2_title](#widget-i18ngemelo-digital-vista-identidadwidget2title-10)           | basic-map-ol   | widget    | i18n_gemelo-digital-vista-identidad_widget_2_description                                                                                                                                                                                                                                                                                                                                                |
| [](#widget--3)                                                                                                            | iframe         | widget    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [i18n_gemelo-digital-vista-identidad_widgets_4_conf_title](#widget-i18ngemelo-digital-vista-identidadwidgets4conftitle-2) | gauge          | widget    | i18n_gemelo-digital-vista-identidad_widgets_4_conf_description                                                                                                                                                                                                                                                                                                                                          |
| [Congestión del tráfico por horas](#widget-congestión-del-tráfico-por-horas-1)                                            | timeseries     | widget    | Distribución de la congestión del tráfico según las horas del día. Se actualiza según los selectores de distrito, tipo de día y temporada.                                                                                                                                                                                                                                                              |
| [Ranking de tramos por congestión](#widget-ranking-de-tramos-por-congestión-1)                                            | horizontal-bar | widget    | Ranking de los tramos con doble ordenación según su congestión (valor medio diario): de más a menos congestionados y de menos a más. Se actualiza según los selectores de distrito, tipo de día y temporada.                                                                                                                                                                                            |
| [IMD por distrito](#widget-imd-por-distrito-1)                                                                            | table          | widget    | Tabla con la intensidad media diaria (IMD) de los 19 distritos de Valencia. Para cada distrito, se muestra la IMD para el tipo de día por defecto (laborable). Se escoge el punto de medida con la IMD más alta. La IMD se obtiene sumando el total de vehículos que transitan por ese punto a lo largo de un año y dividiendo la suma entre los 365 días. Se actualiza con el selector de tipo de día. |
| [Horas pico y valle de tráfico](#widget-horas-pico-y-valle-de-tráfico-1)                                                  | table          | widget    | Detalle de horas pico (mayor probabilidad de congestión) y horas valle (menor probabilidad de congestión) para todos los tramos, con dos franjas diarias (mañana y tarde). Se actualiza con los selectores de distrito, tipo de día y temporada.                                                                                                                                                        |

#### Control: i18n_gemelo-digital-vista-identidad_selector_3_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trend_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "trend"}, "toEvent": "ON_FILTER_TREND"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_1_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_zone_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "zone"}, "toEvent": "ON_FILTER_DISTRICT"}]` |

- **Eventos recibidos**: Ninguno

#### Control: i18n_gemelo-digital-vista-identidad_selector_2_title

- **Descripción**:
- **Tipo**: selector
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_daytype_lastdata"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ON_FILTER | `[{"mapping": {"operator": "operator", "value": "value"}, "stages": ["mapping", "static"], "static": {"var": "daytype"}, "toEvent": "ON_FILTER_DAYTYPE"}]` |

- **Eventos recibidos**: Ninguno

#### Control: *Sin título*

- **Descripción**:
- **Tipo**: refresher
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

- **Eventos recibidos**: Ninguno

#### Widget: Tabs

- **Descripción**:
- **Tipo**: tabs
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                    |
| --------- | ------------------------------------------------ |
| ON_FILTER | `["ON_FILTER_ENTITYID", "ON_FILTER_ENTITYTYPE"]` |
| ON_RELOAD | `ON_RELOAD`                                      |

#### Widget: i18n_gemelo-digital-vista-identidad_widget_2_title

- **Descripción**:
- **Tipo**: basic-map-ol
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "description": "Mapa de Valencia con el estado habitual de los parkings y la fluidez habitual del tr\u00e1fico. Se actualiza seg\u00fan los selectores de distrito, tipo de d\u00eda (laborable, s\u00e1bados, domingos) y temporada. Por defecto muestra el estado para el tipo de d\u00eda laborable.",
    "sources": {
        "emt-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_routeintensity_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-lines": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_trafficcongestion_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        },
        "offstreetparking-location": {
            "connectionProperties": {
                "geomVar": "location",
                "table": "@{prefijo}dtwin_offstreetparking_sim"
            },
            "name": "gemelo_parking",
            "type": "postgresql"
        }
    },
    "type": "multiple"
}
```

- **Eventos emitidos**:

| Slot      | Id del evento        |
| --------- | -------------------- |
| ON_FILTER | `ON_FILTER_ENTITYID` |

- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DISTRICT", "ON_FILTER_DAYTYPE", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: 

- **Descripción**: Nivel medio de congestión del tráfico, en las vías de circulación de la ciudad de Valencia. Se actualiza con los selectores de distrito, tipo de día y temporada.
- **Tipo**: iframe
- **Ubicación**: widget
- **Fuente de datos**: Ninguno
- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento |
| --------- | ------------- |
| ON_RELOAD | `ON_RELOAD`   |

#### Widget: i18n_gemelo-digital-vista-identidad_widgets_4_conf_title

- **Descripción**:
- **Tipo**: gauge
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Congestión del tráfico por horas

- **Descripción**:
- **Tipo**: timeseries
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_yesterday"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: Ranking de tramos por congestión

- **Descripción**:
- **Tipo**: horizontal-bar
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |

#### Widget: IMD por distrito

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "geomVar": "location",
        "table": "@{prefijo}dtwin_trafficintensity_daily"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                    |
| --------- | ---------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND"]` |
| ON_RELOAD | `ON_RELOAD`                                                      |

#### Widget: Horas pico y valle de tráfico

- **Descripción**:
- **Tipo**: table
- **Ubicación**: widget
- **Fuente de datos**:

```json
{
    "connectionProperties": {
        "table": "@{prefijo}dtwin_trafficcongestion_peak"
    },
    "type": "postgresql"
}
```

- **Eventos emitidos**: Ninguno
- **Eventos recibidos**:

| Slot      | Id del evento                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| ON_FILTER | `["ON_FILTER_DAYTYPE", "ON_FILTER_DISTRICT", "ON_FILTER_TREND", "ON_FILTER_MAP"]` |
| ON_RELOAD | `ON_RELOAD`                                                                       |
