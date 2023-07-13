# Distribución óptima de dispositivos de feromonas en plantaciones

Este repositorio contiene código de Python que implementa un algoritmo para encontrar patrones de distribución óptimos de dispositivos de feromonas en plantaciones.
El problema a resolver y la solución implementada se detallan en [`device_patterns.ipynb`](./device_patterns.ipynb).

Adicionalmente, se implementa una API que permite ejecutar el algoritmo y obtener los resultados en formato JSON.
La API puede consumirse directamente, o a través de una interfaz web en https://acarril.github.io/device-patterns.

## Instalación

Clonar este repositorio localmente y crear un entorno virtual con versión de Python indicada en [`.python-version`](./.python-version).
Las dependencias del proyecto se encuentran en [requirements.txt](./requirements.txt), y pueden instalarse con `pip install -r requirements.txt`.

## API

La dirección de la API es https://jix6oc21j7.execute-api.us-east-1.amazonaws.com/api/

Actualmente, para interactuar con la API debe hacerse un POST request a la dirección, y el cuerpo del request debe contener un JSON con los siguientes campos:
- `p`: número entero con la cantidad de plantas
- `d_min`: número entero con densidad mínima de dispositivos

Por ejemplo,
```json
{
    "p": 444,
    "d_min": 200
}
```

La respuesta de la API a un request como el anterior es:
```json
{
    "min_densidad": {
        "densidad": 200.0,
        "patrones": [
            "3/5",
            "1/2",
            "1/4"
        ]
    },
    "min_hileras": {
        "densidad": 204.0,
        "patrones": [
            "2/3",
            "1/4"
        ]
    }
}
```


## Evaluación del algoritmo

![image](./assets/algo_eval_dmin_200.png)
![image](./assets/algo_eval_dmin_300.png)
![image](./assets/algo_eval_dmin_500.png)
