## Instrucciones de instalación manuales

Estas instrucciones solo aplican en el caso de que la vertical se despliegue manualmente. No son necesarias para verticales desplegadas por URBO DEPLOYER.

NOTA: el orden de los ficheros es importante. Los comandos deben ejecutarse en el orden indicado.

Ejecutar los siguientes comandos:

```bash
# Variables utilizadas en los ficheros SQL
export TARGET_HOST="servidor postgres"
export TARGET_PORT="puerto postgres"
export TARGET_DATABASE="nombre bbdd"
export TARGET_SCHEMA="schema bbdd"
export TARGET_USER="usuario bbdd"

# Carga de ficheros SQL
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/daytype_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/offstreetparking_historic.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/offstreetparking_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/routeintensity_historic.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/routeintensity_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/routeschedule_historic.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/routeschedule_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/trafficcongestion_historic.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/trafficcongestion_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/trafficintensity_historic.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/trafficintensity_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/zone_lastdata.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/offstreetparking_join.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/routeintensity_join.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/routeschedule_join.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/trafficcongestion_join.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/trafficintensity_join.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/custom_OffStreetParking.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/custom_RouteIntensity.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/custom_RouteSchedule.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/custom_TrafficCongestion.sql"
psql -1 -h "${TARGET_HOST}" -p "${TARGET_PORT}" -U "${TARGET_USER}" -d "${TARGET_DATABASE}" -v "target_database=${TARGET_DATABASE}" -v "target_schema=${TARGET_SCHEMA}" -v "target_user=${TARGET_USER}" -f "sql/custom_TrafficIntensity.sql"
```

## Ficheros SQL por tipo entidad

### Ficheros SQL asociados al modelo DayType

- **daytype_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo DayType

### Ficheros SQL asociados al modelo OffStreetParking

- **offstreetparking_historic.sql**: Fichero SQL del flujo historic (tipo FLOW_HISTORIC) en modelo OffStreetParking

- **offstreetparking_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo OffStreetParking

- **custom_OffStreetParking.sql**: Conjunto de vistas utilitarias para la presentación de datos de escenarios identidad y simulaciones.

- **offstreetparking_join.sql**: Fichero SQL del flujo join (tipo FLOW_JOIN_VIEW)

### Ficheros SQL asociados al modelo RouteIntensity

- **routeintensity_historic.sql**: Fichero SQL del flujo historic (tipo FLOW_HISTORIC) en modelo RouteIntensity

- **routeintensity_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo RouteIntensity

- **custom_RouteIntensity.sql**: Conjunto de vistas utilitarias para la presentación de datos de escenarios identidad y simulaciones.

- **routeintensity_join.sql**: Fichero SQL del flujo join (tipo FLOW_JOIN_VIEW)

### Ficheros SQL asociados al modelo RouteSchedule

- **routeschedule_historic.sql**: Fichero SQL del flujo historic (tipo FLOW_HISTORIC) en modelo RouteSchedule

- **routeschedule_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo RouteSchedule

- **custom_RouteSchedule.sql**: Conjunto de vistas utilitarias para la presentación de datos de escenarios identidad y simulaciones.

- **routeschedule_join.sql**: Fichero SQL del flujo join (tipo FLOW_JOIN_VIEW)

### Ficheros SQL asociados al modelo TrafficCongestion

- **trafficcongestion_historic.sql**: Fichero SQL del flujo historic (tipo FLOW_HISTORIC) en modelo TrafficCongestion

- **trafficcongestion_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo TrafficCongestion

- **custom_TrafficCongestion.sql**: Conjunto de vistas utilitarias para la presentación de datos de escenarios identidad y simulaciones.

- **trafficcongestion_join.sql**: Fichero SQL del flujo join (tipo FLOW_JOIN_VIEW)

### Ficheros SQL asociados al modelo TrafficIntensity

- **trafficintensity_historic.sql**: Fichero SQL del flujo historic (tipo FLOW_HISTORIC) en modelo TrafficIntensity

- **trafficintensity_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo TrafficIntensity

- **custom_TrafficIntensity.sql**: Conjunto de vistas utilitarias para la presentación de datos de escenarios identidad y simulaciones.

- **trafficintensity_join.sql**: Fichero SQL del flujo join (tipo FLOW_JOIN_VIEW)

### Ficheros SQL asociados al modelo Zone

- **zone_lastdata.sql**: Fichero SQL del flujo lastdata (tipo FLOW_LASTDATA) en modelo Zone
