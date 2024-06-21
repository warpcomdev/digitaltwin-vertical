# Manual de usuario

La vertical del gemelo digital está compuesta de las siguientes vistas principales:

- [Vista identidad](#vistaidentidad): La vista identidad es aquel conjunto de indicadores que mejor caracterizan una ciudad dentro del ámbito de estudio y para el punto de vista de un gestor. Es una vista real, no simulada, pero nueva, diseñada y optimizada para ser la mejor representación de la ciudad, el escenario cero, de referencia. Es el punto de partida del gemelo, ya que determina los conjuntos y modelos de datos que se utilizarán para generar las vistas simuladas.
- [Tablero de simulación](#tablerosimulacion): El tablero de simulación permite la generación de nuevos escenarios, comprendidos dentros de los tipos de simulaciones establecidos actualmente: creación de un nuevo parking, creación de una nueva línea EMT, peatonalización de una calle y corte de una calle de larga duración.
- [Vista simulación] (#tablerosimulacion): Como en la vista de identidad, los widgets de cada una de las pestañas que lo compoenen permiten visualizar rápidamente el estado habitual de los servicios de la ciudad, pero con la diferencia de que estos paneles cuentan con un selector que permite elegir alguna de las simulaciones creadas anteriormente.
- [Vista comparación] (#vistacomparacion): Esta vista consta únicamente de un panel que permite realizar comparaciones en tiempo real entre las simulaciones creadas con anterioridad, así como el escenario por defecto "la vista identidad".

Una vez se ha accedido al entorno, la primera interfaz que se muestra es la de selección de ámbitos (scope_tree), como se corresponde con la siguiente imagen:

![Scope_tree](scope_tree.png)

Después de seleccionar uno de los ámbitos o scopes, es posible navegar entre aquellos paneles que están relacionados con el mismo scope. Para ello, se dispone de dos opciones: 

- La primera es la navegación directa a través de las pestañas o "tabs":

![Tabs](tabs.png)

- La otra posibilidad es clicar en la sección "ir al panel" y desplegar las opciones correspondientes. 

## Vista identidad

 Se divide en cinco secciones o pestañas:

- Estado general
- Parking
- Transporte público
- Tráfico
- Urbanismo

Cada una de ellas refleja una serie de widgets que permiten visualizar rápidamente el estado habitual de los servicios de la ciudad. En el caso concreto de la pestaña "estado general", sirve como punto de partida y resumen general de las demás pestañas.

## Tablero de simulación

 Se divide en cuatro pestañas, que se corresponden con los cuatro escenarios contemplados:

- Nuevo parking
- Nueva línea EMT
- Peatonalización de calle
- Corte de calle de larga duración


## Vista simulación

 Se divide en cinco secciones o pestañas:

- Estado general
- Parking
- Transporte público
- Tráfico
- Urbanismo

Como en la vista de identidad, cada una de ellas refleja una serie de widgets que permiten visualizar rápidamente el estado habitual de los servicios de la ciudad, pero con la diferencia de que estos paneles cuentan con un selector que permite elegir alguna de las simulaciones creadas anteriormente.
Una vez elegida una simulación, los datos que se muestran en los widgets a continuación se corresponden con la perturbación provocada por los parámetros definidos en la simulación. 

## Vista comparación

En último lugar, esta vista consta únicamente de un panel que permite realizar comparaciones en tiempo real entre las simulaciones creadas con anterioridad, así como el escenario por defecto "la vista identidad". 
