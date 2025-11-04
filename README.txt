EL PASADO, PRESENTE Y FUTURO DE LA ENERGÍA NUCLEAR - Programa creado por Franco Baldassarre.

* A partir de datos predeterminados, grafica LCOE, ingresos a lo largo del tiempo y emisiones de CO2.
* El usuario puede cambiar los datos y crear nuevas fuentes (no se almacenan los datos).

--- Propuestas de ampliación --- 
En su forma actual, el programa tiene una función muy básica de almacenar y graficar a partir de datos proporcionados que buscan ser lo más posiblemente precisos, pero que igualmente fluctúan constantemente en el mercado energético. La decisión de hacerlo en Python se debe a su adaptabilidad y su capacidad de integrar programas fácilmente, así que puede ser fácilmente conectado a un programa que calcule, por ejemplo, el beneficio, consiguiendo que tenga datos en tiempo real para hacer predicciones.

Además, el programa podría ser mejorado con métodos matemáticos de la estadística para considerar posibles desviaciones y conseguir datos más realistas. El programa en sí no tiene las mismas tablas que se han mostrado anteriormente (tabla 6 y 7), que muestran los datos en un formato más accesible y que integrarlo en el programa supone un reto pero mejoraría la interactibilidad de la interfaz.

En el aspecto más técnico, las funciones enviar y nuevafuente podrían ser optimizadas evitando la repetición de una cadena condicional y optando por algun tipo de contador que evite tener que actualizar manualmente los diccionarios y estas funciones manualmente cuando se añade una nueva propiedad y lo haga automáticamente. Sería ideal, a su vez, hacer la aplicación adaptable a varios dispositivos y hacer el gráfico interactivo en lugar de que sea una figura.

---------------------------------
