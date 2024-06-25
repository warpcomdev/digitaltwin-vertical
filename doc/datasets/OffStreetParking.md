# Dataset aparcamientos

El Dataset de aparcamientos contiene información sobre la ocupación de un aparcamiento con barrera. Actualmente se soportan aparcamientos cerrados con capacidad constante. La información que debe contener el dataset es:

- `entityid`: ID de aparcamiento.
- `TimeInstant`: Fecha y hora de la medida. Se esperan medidas regulares (por ejemplo con cada variación de la ocupación del parking).
- `occupation`: Ocupación del aparcamiento.
- `capacity`: Capacidad del aparcamiento.

Adicionalmente es necesario un dataset adicional, estático, con información invariante sobre el aparcamiento en cuestión:

- `entityid`: ID del aparcamiento.
- `name`: Nombre descriptivo.
- `location`: Ubicación del aparcamiento (punto geográfico).
- `zone`: Zona a la que se asocia la ubicación anterior.

## Regularización

La regularización de este dataset consiste en aplicar los siguientes cambios:

- `TimeInstant`: se trunca la hora de medida a la hora exacta inmediatamente anterior.
- `occupation`: se asigna como valor de ocupación la **media aritmética** de todos los valores de ocupación de las filas cuyos valores de `TimeInstant` y `entityId` coincidan.

## Identidad

La métrica identidad (caracterización estadística) derivada de este dataset se almacena en las entidades [OffStreetParking](../../assets/model/README.md#OffStreetParking), generándola a partir del dataset anterior con la siguiente lógica:

- Derivamos dimensiones:
    - daytype: ... 
    - trend: ... (estacionalidad)
    - hour: ...

- Agregamos los datos por ID de entidad y conjunto de dimensiones:
    - occupation:
        - media matemática del valor de `occupation`
    - capacity:
        - media matemática del valor de `capacity`
    - occupationPercent:
        - suma del valor de `occupation` / suma del valor de `capacity`

- Actualizamos los atributos de la entidad `OffStreetParking` dada por el entityId:
    - `daytype`
    - `trend`
    ...
