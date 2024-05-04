# Dataset intensidad de tráfico

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
