## Dataset congestión

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
