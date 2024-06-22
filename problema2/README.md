## Problema 2, juego basado en decisión por consenso del tipo p2p

### Especificación de lenguaje

- Python versión 3.11.9: Usado para la creación del servidor y la lógica del juego
- JavaScript: Usado para la comunicación en la parte del cliente y la modificación del html
- Java (JDK-22): Utilizado para leer logs y enviarlos a un servidor central.

### Frameworks utilizados

- Python:
    - flask (v3.0.3): Para la creación de la API
    - flask_socketio (v5.3.6): Extensión de flask para la comunicación bidireccional entre el servidor y los clientes
    - python-dotenv (v1.0.1): Para la lectura de variables de entorno en el archivo .env
    - logging (0.4.9.6): Mecanismo para escrituras de logs de cada cliente

- JavaScript:
    - socket.io (v3.0.5): Para la comunicación desde el cliente al servidor
    - jquery (v2.2.4): Para facilitar la interacción con los componentes HTML

### Variables de entorno - Juego

Contienen información de la lógica del juego

- NROWS: Número de filas del juego.
- NTEAMS: Número de equipos máximo.
- NPLAYERS: Número de jugadores máximo por equipo.
- MIN: Mínimo valor para el dado de cada jugador.
- MAX: Máximo valor para el dado de cada jugador.

### Variables de entorno - Stadistics

- TIME_GAP: Intervalo de tiempo para los gráficos.

### Forma de despliegue

1. Dirigirse a la carpeta rmi/server/
2. Ejecutar:
```start rmiregistry.exe 4000```
3. Compilar archivos:
```javac LogHandler.java```
```javac LogHandlerImpl.java```
```javac Server.java```
4. En la carpeta rmi/client/, compilar archivos:
```javac Client.java```
5. Copiar LogHandler.class en carpeta client/
6. Ejecutar en carpeta server/:
```java Server```
7. Ejecutar en la raíz del proyecto:
```python3 server.py```
8. Redirigirse a la última ruta especificada en el terminal (Ej: http://192.168.1.83:5000)


