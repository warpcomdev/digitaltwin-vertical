# Información accesoria para proyecto gemelo

## Puntos de medida

- `tra_espiras_p.json`: Relación de las coordenadas de las espiras de medida de tráfico de Valencia, en formato json. Extraído de https://opendata.vlci.valencia.es/dataset/intensidad-de-los-puntos-de-medida-de-trafico-espiras-electromagneticas

- `geo_espiras.ipynb`: Notebook que genera un fichero CSV para cargar la información geográfica de las espiras leída del fichero anterior, en una tabla SQL con el siguiente formato:

```sql
CREATE TABLE IF NOT EXISTS parking.coordenadas_espiras
(
    entityid text COLLATE pg_catalog."default" NOT NULL,
    _location geometry,
    idpm integer,
    distrito integer DEFAULT 1,
    CONSTRAINT pk_coordenadas_espiras PRIMARY KEY (entityid)
)
```

Una vez cargados los datos en la tabla, pueden moverse a la tabla roads_imd con:

```sql
UPDATE parking.roads_imd AS p
SET _location = c._location, distrito = c.distrito
FROM parking.coordenadas_espiras AS c
WHERE p.entityid = c.entityid;
```

## Tramos

## Congestión

- `estat-transit-temps-real-estado-trafico-tiempo-real.json`: Datos geográficos de los puntos de medida de congestión. Datos extraídos de https://valencia.opendatasoft.com/explore/dataset/estat-transit-temps-real-estado-trafico-tiempo-real/table/

- `geo_congestion.ipynb`: Notebook que genera un fichero CSV para cargar la información geográfica de las cámaras leída del fichero anterior, en una tabla SQL con el siguiente formato:

```sql
CREATE TABLE IF NOT EXISTS parking.coordenadas_congestion
(
    entityid text COLLATE pg_catalog."default" NOT NULL,
    _location geometry,
    _line geometry,
    idpm integer,
    descripcion text,
    distrito integer DEFAULT 1,
    CONSTRAINT pk_coordenadas_congestion PRIMARY KEY (entityid)
)
```

Una vez cargados los datos en la tabla, pueden moverse a la tabla roads_imd con:

```sql
UPDATE parking.roads AS p
SET _location = c._line, distrito = c.distrito
FROM parking.coordenadas_congestion AS c
WHERE p.entityid = c.entityid;
```
