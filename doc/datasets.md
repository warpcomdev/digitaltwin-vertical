# Datasets

## Introducción

Tanto el análisis estadístico como el aprendizaje predictivo que se realizan en este proyecto se basan en el procesamiento de un conjunto de **datasets**. Cada dataset consiste en un **conjunto de series temporales históricas, monovariables y georeferenciada**, asociadas cada una a un punto de medida. Cada elemento de cada dataset proporciona:

- Un identificador del elemento de medida.
- Una fecha de la medida.
- El valor de la medida.
- Una codificación geográfica del elemento de medida (coordenadas o ID de zona).
- Otras características relevantes del punto de medida, dependiendo del dataset concreto. Ver la descripción de los datasets más adelante.

Los modelos y procedimientos que se definen en este proyecto son aplicables a cualquier ciudad que pueda proporcionar datasets equivalentes a los definidos en esta documentación. 
Todos los datasets que se han usado en este proyecto se basan en el análisis de información real disponible en un caso práctico de cliente de la plataforma Thinking Cities de Telefónica.


## Dataset aparcamientos

### Definición

El Dataset de aparcamientos contiene información sobre la ocupación de un aparcamiento con barrera. Actualmente se soportan aparcamientos cerrados con capacidad constante. La información que debe contener el dataset es:

- `entityid`: ID de aparcamiento.
- `TimeInstant`: Fecha y hora de la medida. Se esperan medidas regulares (por ejemplo con cada variación de la ocupación del parking).
- `occupation`: Ocupación del aparcamiento.

Adicionalmente es necesario un dataset adicional, estático, con información invariante sobre el aparcamiento en cuestión:

- `entityid`: ID del aparcamiento.
- `name`: Nombre descriptivo.
- `capacity`: Capacidad del aparcamiento.
- `location`: Ubicación del aparcamiento (punto geográfico).
- `zone`: Zona a la que se asocia la ubicación anterior.

### Regularización

La regularización de este dataset consiste en aplicar los siguientes cambios:

- `TimeInstant`: se trunca la hora de medida al intervalo de 10 minutos inmediatamente anterior.
- `occupation`: se asigna como valor de ocupación la **media aritmética** de todos los valores de ocupación de las filas cuyos valores de `TimeInstant` y `entityId` coincidan.

## Dataset congestión

### Definición

El Dataset de congestión contiene información sobre el estado congestionado o no congestionado de una vía. Qué se considera *congestión* puede variar en función del proyecto:

- En algunos proyectos, el integrador / proveedor de los datos ya etiqueta la medida como congestionada o no congestionada. Es lo que ocurre en el escenario práctico en el que se basa este proyecto.
- En otros casos, puede ser necesario derivar el valor de otros indicadores primarios, como la velocidad de paso de los vehículos, o la relación entre la intensidad de tráfico instantánea y la intensidad de tráfico media en el tramo.

La información que debe contener el dataset es:

- `entityid`: ID de vía.
- `TimeInstant`: Fecha y hora de la medida. Se esperan medidas frecuentes y regulares (por ejemplo, cada 10 minutos).
- `congestion`: Valor binario, 0 / 1, que indica si el tramo ha sufrido congestión en el intervalo, o no. Se pueden omitir las medidas en las que *congestion == 0*; se entiende que si en un intervalo no hay medida, se puede considerar que no hay congestión.

Adicionalmente es necesario un dataset adicional, estático, con información invariante sobre la vía en cuestión:

- `entityid`: ID de vía.
- `name`: Nombre descriptivo.
- `location`: Ubicación de la vía (punto geográfico).
- `zone`: Zona a la que se asocia la ubicación anterior.
- `line`: Trazado de la vía (geometría tipo `LineString`)

Se considera que cada vía se puede asociar principalmente a una de las zonas en las que se divida la ciudad. No tendría sentido tener una sola medida de congestión para un tramo tan largo que concurra por varias zonas (en caso de existir semejantes tramos, la congestión debería medirse en diferentes puntos a lo largo del mismo, asignando a cada uno un `entityid` distinto).

### Regularización

La regularización de este dataset consiste en aplicar los siguientes cambios:

- `TimeInstant`: se trunca la hora de medida al intervalo de 10 minutos inmediatamente anterior.
- `congestion`: se asigna como valor de congestión el **valor máximo** de todos los valores de congestión de las filas cuyos valores de `TimeInstant` y `entityId` coincidan. Esto es así porque se considera que hay congestión en un intervalo si la hay en cualquier momento dentro de ese intervalo.

## Dataset intensidad de tráfico

### Definición

El Dataset de intensidad de tráfico contiene información sobre el número de vehículos que circula por una vía.

Obviamente, el número de vehículos que usan la vía dependen del intervalo de medida que se considere. En el caso práctico analizado, cada medida proporcionada por los sensores representa una **estimación del IMD (intensida media diaria) extrapolada** de la información que el sensor ha recogido en el último intervalo.

Es decir, si el sensor reporta una medida con el valor `300`, significa que el sensor estima que *de mantenerse todo el día la intensidad de tráfico tal y como ha estado en el último intervalo*, el número de vehículos que pasaría en total a lo largo del día sería `300`.

Teniendo en cuenta esta peculiaridad en cómo se miden las intensidades de tráfico, lo que debe contener este dataset es:

- `entityid`: ID de vía.
- `TimeInstant`: Fecha y hora de la medida. Se esperan medidas regulares (por ejemplo, cada hora).
- `intensity`: Proyección a 24 horas de la intensidad media estimada por el sensor según sus datos más recientes. Es decir, si el sensor ha medido por ejemplo 40 vehículos en el último intervalo de 20 minutos, el valor de la medida debería ser `24 horas * (60 minutos / 20 minutos) * 40 vehículos = 2880`.

Adicionalmente es necesario un dataset adicional, estático, con información invariante sobre la vía en cuestión:

- `entityid`: ID de vía.
- `name`: Nombre descriptivo.
- `location`: Ubicación de la vía (punto geográfico).
- `zone`: Zona a la que se asocia la ubicación anterior.
- `line`: Trazado de la vía (geometría tipo `LineString`)

Se considera que cada vía se puede asociar principalmente a una de las zonas en las que se divida la ciudad. No tendría sentido tener una sola medida de congestión para un tramo tan largo que discurra por varias zonas (en caso de existir semejantes tramos, la congestión debería medirse en diferentes puntos a lo largo del mismo, asignando a cada uno un `entityid` distinto).

### Regularización 

La regularización de este dataset consiste en aplicar los siguientes cambios:

- `TimeInstant`: se trunca la hora de medida al intervalo de 10 minutos inmediatamente anterior.
- `intensity`: se asigna como valor de intensidad la **media aritmética** de todos los valores de intensidad de las filas cuyos valores de `TimeInstant` y `entityId` coincidan.

## Dataset frecuencia de paso de tte. público

### Definición

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

## Dataset uso del tte. público

### Descripción

El Dataset de uso de transporte público contiene información sobre el número de viajeros que utilizan las diferentes líneas de transporte público de la ciudad.

En el caso práctico se ha comprobado que no necesariamente se contará con información detallada de número de viajeros por trayecto o por parada, de forma que este dataset contiene una información más agregada. La información que contiene este dataset es:

- `entityid`: ID de línea.
- `TimeInstant`: Fecha y hora de la medida. Se esperan medidas puntuales (datos agregados horarios o diarios).
- `forwardTrips`: Cantidad de trayectos de ida que se agrupan en la medida.
- `returnTrips`: Cantidad de trayectos de vuelta que se agrupan en la medida.
- `intensity`: Número de usuarios total de los trayectos dados.

Adicionalmente se reutiliza el dataset estático de rutas que se definió en el punto anterior, con información invariante sobre la línea en cuestión.

### Regularización

Por la forma en que se obtienen los datos en el caso de estudio, para este dataset solo hay una medida diaria por entidad. De forma que no es necesaria regularización.
