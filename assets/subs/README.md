Los parámetros con formato `${...}` no han de ser interpretados literalmente, sino que indican un parámetro variable que ha de ser sustituido con aquel que aplique al despliegue concreto cuando se creen las subscripciones indicadas en esta documentación.

# Suscripción a DayType LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo DayType

- **Estado** : Activa
- **Descripción**: DayType:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, alterationType
- **Condición**: TimeInstant
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate, entityDelete
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: DayType

# Suscripción a OffStreetParking HISTORIC

Subscripción del flujo historic (tipo FLOW_HISTORIC) en modelo OffStreetParking

- **Estado** : Activa
- **Descripción**: OffStreetParking:HISTORIC:dtwin:historic
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, capacity, occupationPercent, occupation
- **Condición**: sourceRef, TimeInstant, sceneRef, trend, dayType, hour
  - **Y se cumpla una expresion compuesta por q, mq, georel, geometry y coords**: `{"q": "sceneRef"}`
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: OffStreetParking

# Suscripción a OffStreetParking LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo OffStreetParking

- **Estado** : Activa
- **Descripción**: OffStreetParking:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, name, zone, capacity, location, alterationType
- **Condición**: TimeInstant, sourceRef
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: OffStreetParking

# Suscripción a RouteIntensity HISTORIC

Subscripción del flujo historic (tipo FLOW_HISTORIC) en modelo RouteIntensity

- **Estado** : Activa
- **Descripción**: RouteIntensity:HISTORIC:dtwin:historic
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, forwardStops, returnStops, forwardTrips, returnTrips, intensity
- **Condición**: sourceRef, TimeInstant, sceneRef, trend, dayType
  - **Y se cumpla una expresion compuesta por q, mq, georel, geometry y coords**: `{"q": "sceneRef"}`
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: RouteIntensity

# Suscripción a RouteIntensity LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo RouteIntensity

- **Estado** : Activa
- **Descripción**: RouteIntensity:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, name, zoneList, forwardStops, returnStops, location, alterationType
- **Condición**: TimeInstant, sourceRef
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: RouteIntensity

# Suscripción a RouteSchedule HISTORIC

Subscripción del flujo historic (tipo FLOW_HISTORIC) en modelo RouteSchedule

- **Estado** : Activa
- **Descripción**: RouteSchedule:HISTORIC:dtwin:historic
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, forwardStops, returnStops, forwardTrips, returnTrips
- **Condición**: sourceRef, TimeInstant, sceneRef, trend, dayType, hour
  - **Y se cumpla una expresion compuesta por q, mq, georel, geometry y coords**: `{"q": "sceneRef"}`
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: RouteSchedule

# Suscripción a RouteSchedule LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo RouteSchedule

- **Estado** : Activa
- **Descripción**: RouteSchedule:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, name, zoneList, forwardStops, returnStops, location, alterationType
- **Condición**: TimeInstant, sourceRef
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: RouteSchedule

# Suscripción a Simulation LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo Simulation

- **Estado** : Activa
- **Descripción**: Simulation:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sceneref, name, description, alterationType
- **Condición**: TimeInstant
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate, entityDelete
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: Simulation

# Suscripción a SimulationParking JENKINS

Subscripción del flujo etl (tipo FLOW_RAW) en modelo SimulationParking

- **Estado** : Activa
- **Descripción**: SimulationParking:JENKINS::etl
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente al JENKINS en el entorno>/etl_digitaltwin_vectorize/buildWithParameters", "headers": {"Authorization": "Basic !!{JENKINS_BASIC_AUTH}"}, "qs": {"ETL_VECTORIZE_SIMULATION_TYPE": "${type}", "ETL_VECTORIZE_SIMULATION_ID": "${id}"}, "payload": null}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant
- **Condición**: TimeInstant
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: SimulationParking

# Suscripción a SimulationRoute JENKINS

Subscripción del flujo etl (tipo FLOW_RAW) en modelo SimulationRoute

- **Estado** : Activa
- **Descripción**: SimulationRoute:JENKINS::etl
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente al JENKINS en el entorno>/etl_digitaltwin_vectorize/buildWithParameters", "headers": {"Authorization": "Basic !!{JENKINS_BASIC_AUTH}"}, "qs": {"ETL_VECTORIZE_SIMULATION_TYPE": "${type}", "ETL_VECTORIZE_SIMULATION_ID": "${id}"}, "payload": null}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant
- **Condición**: TimeInstant
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: SimulationRoute

# Suscripción a SimulationTraffic JENKINS

Subscripción del flujo etl (tipo FLOW_RAW) en modelo SimulationParking

- **Estado** : Activa
- **Descripción**: SimulationParking:JENKINS::etl
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente al JENKINS en el entorno>/etl_digitaltwin_vectorize/buildWithParameters", "headers": {"Authorization": "Basic !!{JENKINS_BASIC_AUTH}"}, "qs": {"ETL_VECTORIZE_SIMULATION_TYPE": "${type}", "ETL_VECTORIZE_SIMULATION_ID": "${id}"}, "payload": null}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant
- **Condición**: TimeInstant
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: SimulationParking

# Suscripción a TrafficCongestion HISTORIC

Subscripción del flujo historic (tipo FLOW_HISTORIC) en modelo TrafficCongestion

- **Estado** : Activa
- **Descripción**: TrafficCongestion:HISTORIC:dtwin:historic
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, minute, congestion
- **Condición**: sourceRef, TimeInstant, sceneRef, trend, dayType, hour, minute
  - **Y se cumpla una expresion compuesta por q, mq, georel, geometry y coords**: `{"q": "sceneRef"}`
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: TrafficCongestion

# Suscripción a TrafficCongestion LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo TrafficCongestion

- **Estado** : Activa
- **Descripción**: TrafficCongestion:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, name, zone, location, alterationType
- **Condición**: TimeInstant, sourceRef
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: TrafficCongestion

# Suscripción a TrafficIntensity HISTORIC

Subscripción del flujo historic (tipo FLOW_HISTORIC) en modelo TrafficIntensity

- **Estado** : Activa
- **Descripción**: TrafficIntensity:HISTORIC:dtwin:historic
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, intensity
- **Condición**: sourceRef, TimeInstant, sceneRef, trend, dayType, hour
  - **Y se cumpla una expresion compuesta por q, mq, georel, geometry y coords**: `{"q": "sceneRef"}`
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: TrafficIntensity

# Suscripción a TrafficIntensity LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo TrafficIntensity

- **Estado** : Activa
- **Descripción**: TrafficIntensity:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sourceRef}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, name, zone, location, alterationType
- **Condición**: TimeInstant, sourceRef
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: TrafficIntensity

# Suscripción a Trend LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo Trend

- **Estado** : Activa
- **Descripción**: Trend:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, alterationType
- **Condición**: TimeInstant
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate, entityDelete
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: Trend

# Suscripción a Zone LASTDATA

Subscripción del flujo lastdata (tipo FLOW_LASTDATA) en modelo Zone

- **Estado** : Activa
- **Descripción**: Zone:LASTDATA:dtwin:lastdata
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, zoneId, name, label, location, alterationType
- **Condición**: TimeInstant
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate, entityDelete
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: Zone
