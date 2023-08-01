# Asesoría para automatizar la generación de patrones óptimos de instalación de dispositivos

### Álvaro Carril, Ph.D. (c)

Esta asesoría tiene como objetivo automatizar la generación de patrones de distribución óptimos para la instalación de dispositivos en plantaciones.
La implementación de una solución completa del problema requiere de los siguientes componentes:

1. Modelamiento matemático del problema y descripción de un algoritmo de optimización para encontrar una solución óptima, sujeto a un conjunto de restricciones
2. Programa que implemente el algoritmo de optimización
3. API que exponga la funcionalidad del programa anterior, para que pueda ser consumida por un _front-end_ (aplicación web u otro)
4. _Front-end_ que permita a un usuario interactuar con la API y visualizar la solución a un problema con parámetros dados

Cada uno de estos componentes, en conjunto con la documentación correspondiente, sugiere un conjunto de entregables.
Se detallan las horas de trabajo y/o desarrollo junto con el costo asociado a cada uno de ellos en la siguiente tabla:

|                             | Horas | Costo (UF) |
|-----------------------------|------:|-----------:|
| 1. Modelamiento             |     3 |          9 |
| 2. Software de optimización |     8 |         24 |
| 3. REST API                 |     2 |          6 |
| 4. Front-end                |     3 |          9 |
| **Total**                   |**16** |     **48** |

## Entregables

Al tratarse de un proyecto de _software_, todo el material a entregar se reunirá en el repositorio Github del proyecto.

1. El modelamiento matemático del problema junto con la descripción del algoritmo de optimización se entregará en un documento en formato Markdown.
2. El software de optimización se implementará en el lenguaje de programación Python.
3. A su vez, la API se implementará en Python, utilizando el framework Chalice/Flask. El _stack_ de desarrollo se desplegará en AWS Lambda, usando API Gateway para generar una URL pública para la API.
4. El _front-end_ se implementará en HTML/CSS simple y Javascript, y se desplegará en una página web estática en Github Pages.

El resultado final de la asesoría corresponde a una página web estática donde un usuario podrá ingresar los parámetros de un problema, y visualizar la solución óptima a dicho problema.
