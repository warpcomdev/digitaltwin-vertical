# Dataset aparcamientos

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

## Regularización

La regularización de este dataset consiste en aplicar los siguientes cambios:

- `TimeInstant`: se trunca la hora de medida al intervalo de 10 minutos inmediatamente anterior.
- `occupation`: se asigna como valor de ocupación la **media aritmética** de todos los valores de ocupación de las filas cuyos valores de `TimeInstant` y `entityId` coincidan.
