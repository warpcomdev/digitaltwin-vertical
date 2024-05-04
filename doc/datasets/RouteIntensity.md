# Dataset uso del tte. público

## Descripción

El Dataset de uso de transporte público contiene información sobre el número de viajeros que utilizan las diferentes líneas de transporte público de la ciudad.

En el caso práctico se ha comprobado que no necesariamente se contará con información detallada de número de viajeros por trayecto o por parada, de forma que este dataset contiene una información más agregada. La información que contiene este dataset es:

- `entityid`: ID de línea.
- `TimeInstant`: Fecha y hora de la medida. Se esperan medidas puntuales (datos agregados horarios o diarios).
- `forwardTrips`: Cantidad de trayectos de ida que se agrupan en la medida.
- `returnTrips`: Cantidad de trayectos de vuelta que se agrupan en la medida.
- `intensity`: Número de usuarios total de los trayectos dados.

Adicionalmente se reutiliza el dataset estático de rutas que se definió en el punto anterior, con información invariante sobre la línea en cuestión.

## Regularización

Por la forma en que se obtienen los datos en el caso de estudio, para este dataset solo hay una medida diaria por entidad. De forma que no es necesaria regularización.
