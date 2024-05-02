Los contenidos de este directorio son ficheros con entidades de referencia de tipo Vertical en formato NGSIv2 normalized, siguiendo el siguiente patrón de nombrado:

> vertical-`<id de entidad>`[-upgradefrom-`<version origen>`].json

donde:

- `<id de entidad>` sigue el siguiente patrón: `<nombre vertical camelCase>_<número de versión>[_<flavour>]`, siendo el `<flavour>` (en camelCase) un elemento opcional, que dependerá de si el vertical tiene definidos sabores o no.
- `upgradefrom-<version origen>` cuando aparece indica que la entidad incluye el "delta" de upgrade en los atributos `upgrades` y `upgradesList` correspondiente al upgrade desde `<version origen>`.

El contenido de estos ficheros es directamente usable en una petición de tipo upsert en la API NGSIv2 del Context Broker (ie. `POST /v2/entities?options=upsert`) en el sevicio/subservicio que contenga las entidades de tipo Vertical.
