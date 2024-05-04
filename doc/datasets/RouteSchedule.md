# Dataset frecuencia de paso de tte. público

El Dataset de frecuencia de paso de transporte público contiene información sobre la planificación de las diferentes líneas de transporte público de la ciudad.

Aunque quizá la información más directa que se podría esperar de este dataset es una lista de horarios de salida, en el caso práctico en el que se basa este proyecto se ha comprobado que lo habitual, al menos en el caso de servicios integrados con Google Transit, es disponer de una **parrilla de programación** en la que indica con qué frecuencia salen autobuses, en función de la franja horaria.

Dado que las líneas tienen dos trayectos (ida y vuelta), y por consistencia todos los datasets deben ser monovariables, para este servicio definimos dos datasets:

- **idas**:
    - `entityid`: ID de línea.
    - `start`: Hora de inicio el intervalo de medida. Se esperan medidas puntuales (pocos cambios en la parrila a lo largo del día).
    - `end`: Hora de fin del intervalo de medida.
    - `forwardTrips`: Número de trayectos de ida en el intervalo.

- **vueltas**:
    - `entityid`: ID de línea.
    - `start`: Hora de inicio el intervalo de medida. Se esperan medidas puntuales (pocos cambios en la parrila a lo largo del día).
    - `end`: Hora de fin del intervalo de medida.
    - `returnTrips`: Número de trayectos de ida en el intervalo.

Adicionalmente es necesario un dataset adicional, estático, con información invariante sobre la línea en cuestión:

- `entityid`: ID de línea.
- `name`: Nombre descriptivo.
- `line`: Trazado de la vía (geometría tipo `LineString`)
- `zones`: Lista de zonas por las que pasa la línea.
- `forwardStops`: Número de paradas en el trayecto de ida.
- `returnStops`: Número de paradas en el trayecto de ida.

Nota: no se incluye en el dataset el número de paradas por zona, ya que en el caso práctico de estudio no existe ninguna información asociada a paradas individuales.

### Regularización

La regularización de este dataset consiste en aplicar los siguientes cambios:

- `TimeInstant`: Se asigna a cada fila un valor de `TimeInstant` = `start` truncado a la hora anterior.
  - Se replica cada fila una vez por cada hora, incrementando `TimeInstant` en intervalos de 1 hora hasta superar a `stop`.
  - Se reparten proporcionalmente los valores de `forwardTrips`, `returnTrips` e `intensity` entre todas las filas creadas.
- `forwardTrips`: Se asigna como valor **la suma** de todos los valores de forwardTrips de las filas cuyos valores de `TimeInstant` y `entityId` coincidan.
- `returnTrips`: Se asigna como valor **la suma** de todos los valores de forwardTrips de las filas cuyos valores de `TimeInstant` y `entityId` coincidan.
