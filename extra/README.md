# Setup de entorno demo

Para utilizar la vertical, es imprescindible contar con un conjunto inicial de datos (*vista identidad*) que se extrae de los datasets descritos en la [documentación general](../doc/README.md).

En un entorno de demo, típicamente no se dispone de un histórico de datos suficientes para construir esos datasets, de manera que la vertical incluye un listado de CSVs con información extraída del caso de uso utilizado en el desarrollo (Valencia), que puede importarse en la plataforma para pre-cargar una vista identidad sobre la que hacer simulaciones.

Los CSVs a importar en un entorno demo son los que se encuentran en el directorio [csvs](./csvs):

- AirQualityObserved.csv
- DayType.csv
- OffStreetParking.csv
- RouteIntensity.csv
- RouteSchedule.csv
- Simulation.csv
- TrafficCongestion.csv
- TrafficIntensity.csv
- Trend.csv
- Zone.csv
