# Schema de entidades

Esta vertical se construye principalmente en torno a dos tipos de entidades:

- Las entidades **gemelo**: Representan un servicio de la ciudad, que queremos representar en el gemelo digital (ek: aparcamientos, tráfico, rutas de transporte público)
- Las entidades **simulación**: Representan un conjunto de parámetros que afectan a las simulaciones que queremos hacer sobre los servicios anteriores.

Cada tipo de entidad tiene ciertas características y comportamientos que son comunes a otras entidades del mismo tipo, y también características propias que se corresponden con el servicio o simulación que están modelando.

Para formalizar de la manera más estricta posible las características que definen a las entidades de uno y otro tipo, y garantizar la consistencia entre ellas, se han utilizado [schemas cue](https://cuelang.org/) que definen de manera formal estas características y comportamiento.

## Entidades de tipo gemelo

Los tipos de entidad que representan servicios del gemelo son instancias del patrón [templates/twin.cue](./templates/twin.cue). Este patrón se basa en la definición de tres tipos de atributos:

- **dimensiones**: Son atributos comunes a todas estas entidades. Estas dimensiones permiten filtrar y agregar los datos de manera consistente cuando se combinan entidades de varios tipos en un mismo panelSon:

  - `sourceRef`: ID de la entidad original, de la que esta entidad simulada es un espejo.
  - `sceneRef`: Escenario de simulación al que pertenece la medida.
  - `dayType`: tipo de día.
  - `trend`: estacionalidad.
  - `name`: Nombre de la entidad.
  - `location`: UBicación de la entidad.
  - `zone`: Partición geográfica (por ejemplo, distrito) al que pertenece la entidad.

- **métricas**: Representan los datos de cada servicio que se modelan en el gemelo (ocupación del parking, intensidad del tramo de tráfico, etc), además de la referencia temporal a la que se refiere el dato:

  - `hour` (opcional): hora a la que corresponde la medida. Solo aplica a servicios que se modelan con granularidad horaria.
  - `minute` (opcional): minuto al que corresponde la medida. Solo aplica a servicios que se modelan con granularidad homa-minuto.

  **NOTA**: En esta vertical, la fecha a la que se refiere un dato está determinada por el conjunto de atributos `dayType`, `trend`, `hour`, `minute`. El atributo `TimeInstant` no determina la fecha del dato, ya que los datos son *atemporales* (Están categorizados por estacionalidad y tipo de día, no por una fecha concreta).
  
  En su lugar, `TimeInstant` determina la fecha en la que se ejecutó la simulación, y se considera una **dimensión**, es decir, un criterio de agrupación y filtrado pero no una referencia temporal. Todas las medidas de una misma simulación tienen en mismo `TimeInstant`.

- **propiedades**: Representan atributos específicos de un servicio en concreto, pero que no son métricas (no son modeladas). Por ejemplo, el número de paradas de una línea de transporte público no es algo que se modifique en las simulaciones, pero tampoco es algo común a todos los tipos de servicio.

Al utilizar la plantilla [twin.cue](./templates/twin.cue), garantizamos que todos los tipos de entidades que representan servicios tienen una estructura consistente tanto en base de datos (tablas histórica, lastdata, y vistas necesarias para los paneles de simulación) como en plataforma (suscripciones y reglas CEP).

## Entidades de tipo simulación

Los tipos de entidad que representan escenarios de simulación son instancias del patrón [templates/simulation.cue](./templates/simulation.cue). Este patrón define los **atributos comunes** a cualquier simulación:

- `TimeInstant`: Fecha de la simulacion
- `name`: Nombre de la nueva simulación
- `description`: Descripción de la nueva simulación
- `bias`: Bias a aplicar en la simulación
- `status`: Estado de la simulación

Y los comportamientos comunes a cualquier simulación, que en este caso consisten en el flujo que dispara al notificación a Jenkins para ejecutar la simulación.
