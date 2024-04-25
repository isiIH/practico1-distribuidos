## Problema 1 (HTTP), biblioteca digital distribuida por tipo de documento

### Especificación de lenguaje

- Python versión 3.11.9

### Frameworks utilizados

- flask: Para la creación de la API
- requests: Para la generación de consultas a los nodos esclavos
- psycopg2: Para la comunicación con la base de datos postgres

### Archivos de configuración

Contienen información sobre los nodos esclavos y la configuración con la base de datos

- host: La dirección IP del host donde se encuentra el servidor.
- port: El puerto en el que el servidor está escuchando.
- server_name: El nombre del servidor.
- db_name: El nombre de la tabla dentro de la base de datos que se está utilizando (las particiones se simulan a través de tablas).
- dbConnConfig: Contiene la configuración de conexión a la base de datos, con los siguientes datos:
  - user: El nombre de usuario.
  - pass: La contraseña del usuario.
  - host: La dirección IP del host.
  - port: El puerto en el que la base de datos está escuchando.
  - dbname: El nombre de la base de datos.

### Variables de entorno

Contienen información de la base de datos

 - POSTGRES_USER: Nombre del usuario
- POSTGRES_PASSWORD: Contraseña del usuario
- POSTGRES_DB: Nombre de la base de datos
- POSTGRES_PORT: Puerto en el que la base de datos está escuchando
- POSTGRES_HOST: Dirección IP del host

### Forma de despliegue

1. Dentro de la carpeta /slaves, ejecuta el siguiente comando para levantar la base de datos: 
```docker-compose up -d```
2. Ejecuta los nodos esclavos dentro de la carpeta /slaves en cada terminal:
```python
python3 main.py config/config0.json
python3 main.py config/config1.json
python3 main.py config/config2.json
python3 main.py config/config3.json
```
3. Ejecuta el nodo maestro dentro de la carpeta /master:
```python3 app.py```
4. Accede a la API en http://127.0.0.1:5000
5. Realiza una consulta:
    - http://127.0.0.1:5000/query?titulo=tesis+1
    - http://127.0.0.1:5000/query?tipo_doc=tesis