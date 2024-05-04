# Gemelo Digital

## Introducción

Este repositorio contiene los modelos, procesos y aplicaciones definidos para la creación de un gemelo digital de ciudad.

El concepto de "gemelo digital" se utiliza en múltiples contextos (industria, I+D, economía, modelado 3D, etc) y tiene muchísimas acepciones distintas. En este proyecto, nos referimos concretamente por *gemelo digital* a:

- Una **caracterización estadística** del comportamiento los servicios públicos o métricas de una ciudad (ejemplos: intensidad del tráfico, probabilidad de congestión de las principales vías, etc), que proporciona información sobre los patrones habituales que sigue dicho servicio en diferentes momentos o diferentes zonas de la ciudad. A esta caracterización la denominamos **identidad** de la ciudad.

- Un **modelo matemático** que predice cambios en dicha caracterización, a largo plazo, como consecuencia de modificaciones urbanísticas, regulatorias, etc. Este modelo utiliza un conjunto de supuestos (**escenarios**) para calcular variaciones en la caracterización de la ciudad (**simulación**).

## Datasets

Tanto el análisis estadístico como el aprendizaje predictivo que se realizan en este proyecto se basan en el procesamiento de un conjunto de **datasets**. Cada dataset consiste en un **conjunto de series temporales históricas, monovariables y georeferenciadas**, asociadas cada una a un punto de medida. Cada elelemto de cada dataset proporciona:

- Un identificador del elemento de medida.
- Una fecha de la medida.
- El valor de la medida.
- Una codificación geográfica del elemento de medida (coordenadas o ID de zona).
- Otras características relevantes del punto de medida, dependiendo del dataset concreto. Ver la descripción de los datasets más adelante.

Los modelos y procedimientos que se definen en este proyecto son aplicables a cualquier ciudad que pueda proporcionar datasets equivalentes a los definidos en esta documentación. 
Todos los datasets que se han usado en este proyecto se basan en el análisis de información real disponible en un caso práctico de cliente de la plataforma Thinking Cities de Telefónica.

Los detalles de los datasets soportados se proporcionan en los siguientes documentos:

- [Dataset de aparcameintos](datasets/OffStreetParking.md)
- [Dataset de intensidad de tráfico](datasets/TrafficIntensity.md)
- [Dataset de congestión de tráfico](datasets/TrafficCongestion.md)
- [Dataset de frecuencia de paso de rutas](datasets/RouteSchedule.md)
- [Dataset de uso de rutas](datasets/RouteIntensity.md)

## Clasificación

El concepto de gemelo que se utiliza en este proyecto se basa en la presunción de que los datos de cada uno de los datasets anteriores se ajustan a un número finito de **patrones**, que se repiten en el tiempo.

Por ejemplo, si exceptuamos circunstancias especiales como festivos, se asume que las métricas de un cierto tramo de carretera se parecerán mucho de una semana a la siguiente. El tráfico de un martes normal debería parecerse razonablemente al del martes anterior, o al del miércoles siguiente. Pero puede ser sustancialmente distinto al de un domingo.

También es posible esperar cierta estacionalidad anual en las métricas. Por ejemplo, el tráfico de un lunes típico de invierno puede ser más denso que el de uno de verano, si los ciudadanos tienden a usar más el transporte privado con el mal tiempo.

El objetivo de la primera parte del gemelo, la **caracterización estadística**, es determinar estos patrones: Identificar qué circunstancias se reflejan en el comportamiento observable de la ciudad, y representar de manera visual cuál es el comportamiento de la ciudad en esa circunstancia.

### Regularización de datasets

Las medidas obtenidas de los datasets originales tienen fechas que en general no coinciden para los diferentes puntos de medida, ni para los diferentes días, ni están espaciadas regularmente.

Esto hace imposible una clasificación directa de las series temporales de cada dataset. Para poder comparar unos días con otros, es necesario regularizar los datasets previamente.

La regularización consiste en garantizar que cada dataset tiene el mismo número de muestras por cada punto de medida y día. Esto se hace mediante un resampling de las series temporales a intervalos fijos, que por convención se fijan en **10 minutos**.

Se utilizan diferentes métodos de resampling para cada dataset, en función de sus características.

### Tipos de día

El primer criterio de clasificación es el **tipo de día**. Cada uno de los datasets que se utiliza en el proyecto es una serie temporal univariable. Si se representan para cada dataset varios días consecutivos en un mismo punto de medida, se observarán varios grupos de días que se parecen entre sí.

![tipos de día](doc/notebook/daytype.png)

El objetivo de la clasificación es identificar estos patrones. Formalmente,

- Se normalizan las series temporales regularizadas, restando y escalando cada serie por el valor medio de los últimos 30 días, para minimizar los efectos de la estacionalidad al compararlas entre sí a lo largo del año.

- Se aplica el algoritmo [Time Series Clustering mediante K-means](https://www.kaggle.com/code/izzettunc/introduction-to-time-series-clustering) sobre las series temporales regularizadas, para dividirlas en un número fijo de clusters `N_CLUSTERS`, dado como parámetro.

- Se descartan en cada cluster las series temporales que sean "outliers", considerando como outlier toda serie cuya distancia a la línea de centro de su cluster sea superior al percentil 90% de las distancias.

- Se observan las fechas que forman parte de cada grupo, para identificar relaciones de calendario entre las fechas que forman cada grupo.

Del análisis realizado en el caso práctico, se ha encontrado que la inmensa mayoría de los puntos de medida de todos los datasets se adaptan a una clasificación en cuatro tipos de día:

- Lunes a Jueves
- Viernes
- Sábado
- Domingo

Durante el análisis del caso práctico concluimos que esta clasificación es lo que tiene más sentido y sería aplicable a cualquier otro proyecto de ciudad, sin necesidad de repetir el análisis.

### Estacionalidad

El segundo criterio de clasificación es la estacionalidad. Si se cacula para cada dataset el valor medio mensual y su varianza por cada punto de medida, los valores medios se pueden alinear en una matriz que indique cuánto se diferencia porcentualmente de un mes de otro.

Estableciendo un umbral límite para la variación porcentual, se pueden distinguir grupos de meses que se mantienen dentro de los umbrales cuando e comparan entre sí, pero los exceden al compararse con otros.

Estos grupos se usan como criterio para discriminar por estacionalidad. Típicamente se esperan al menos dos estacionalidades distintas:

- Julio y Agosto
- Resto del año

Aunque en cada ciudad puede variar, por ejemplo: en una ciudad con estaciones de esquí importantes, diciembre, enero y febrero pueden formar otro grupo de estacionalidad.

## Identidad

## Codificación

## Simulación
