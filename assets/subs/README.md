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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, zone, capacity, occupationPercent, occupation
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, name, hour, zone, capacity, occupationPercent, location, occupation, alterationType
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, zoneList, forwardTrips, returnTrips, forwardStops, returnStops, intensity
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, name, zoneList, forwardTrips, returnTrips, forwardStops, returnStops, location, intensity, alterationType
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, zoneList, forwardTrips, returnTrips, forwardStops, returnStops
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, name, hour, zoneList, forwardTrips, returnTrips, forwardStops, location, returnStops, alterationType
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour
  - Tipo de alteration en entidad que desencadena la notificación: entityUpdate, entityCreate
- **Entidades**:
  - ID: `.*` (con checkbox de patrón de búsqueda marcado)
  - Type: RouteSchedule

# Suscripción a TrafficCongestion HISTORIC

Subscripción del flujo historic (tipo FLOW_HISTORIC) en modelo TrafficCongestion

- **Estado** : Activa
- **Descripción**: TrafficCongestion:HISTORIC:dtwin:historic
- **Fecha y hora de expiración**: en blanco
- **Segundos entre notificaciones**: en blanco
- **Protocolo**: HTTP
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}_${minute}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, minute, zone, congestion
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour, minute
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}_${minute}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, name, hour, minute, zone, congestion, location, alterationType
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour, minute
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-HISTORIC en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, hour, zone, intensity
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour
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
- **Notificación personalizada**: `{"url": "<endpoint correspondiente a CYGNUS-LASTADATA en el entorno>", "headers": {"fiware-servicepath": "/dtwin"}, "ngsi": {"id": "${sceneRef}_${sourceRef}_${trend}_${dayType}_${hour}"}}`
- **Formato de atributos**: normalized
- **Atributos a notificar**: TimeInstant, sourceRef, sceneRef, trend, dayType, name, hour, zone, intensity, location, alterationType
- **Condición**: TimeInstant, sceneRef, sourceRef, trend, dayType, hour
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
