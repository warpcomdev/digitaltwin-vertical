# digitaltwin-vertical

Repositorio que contiene la implementación de la vertical `digitaltwin` desarrollada para el proyecto de gemelo digital asociado a la ciudad de Valencia.

Esta vertical tiene dos *flavours*:

- `basic`: Contiene todo el modelo de datos y la lógica necesarios para implementar al vertical en un entorno. Este *flavour* debe desplegarse en primer lugar.
- `preload`: Contiene un conjunto inicial de datos de ejemplo a utilizar para inicializar la vertical. Este *flavour* debe desplegarse, una vez completado el despliegue del anterior, si se quiere precargar un conjunto de datos de prueba (para entornos de demostración, por ejemplo).
