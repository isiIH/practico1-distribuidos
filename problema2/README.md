## Problema 2, juego basado en decisión por consenso del tipo p2p

### Especificación de lenguaje

- Python versión 3.11.9: Usado para la creación del servidor y la lógica del juego
- JavaScript: Usado para la comunicación en la parte del cliente y la modificación del html

### Frameworks utilizados

- Python:
    - flask (v3.0.3): Para la creación de la API
    - flask_socketio (v5.3.6): Extensión de flask para la comunicación bidireccional entre el servidor y los clientes
    - python-dotenv (v1.0.1): Para la lectura de variables de entorno en el archivo .env

- JavaScript
    - socket.io (v3.0.5): Para la comunicación desde el cliente al servidor
    - jquery (v2.2.4): Para facilitar la interacción con los componentes HTML


### Variables de entorno

Contienen información de la lógica del juego

- NROWS: Número de filas del juego.
- NTEAMS: Número de equipos máximo.
- NPLAYERS: Número de jugadores máximo por equipo.
- MIN: Mínimo valor para el dado de cada jugador.
- MAX: Máximo valor para el dado de cada jugador.

### Forma de despliegue

1. Ejecutar en la raíz del proyecto:
```python3 server.py```
2. Redirigirse a la última ruta especificada en el terminal (Ej: http://192.168.1.83:5000)