# Aplicación web de Películas con Flask

Programa hecho en Python con el framework Flask.

Permite:
- Buscar películas por título y año (OMDb API)
- Ver detalle de cada película
- Añadir comentarios
- Ver comentarios guardados (SQLite)

# Instalación

- Crear un entorno virtual en Python, activarlo y ejecutar:

pip install -r requirements.txt

Librerías principales utilizadas:
- Flask
- requests
- SQLite (incluido en Python)

# Configuración

En el archivo appchanges/config.py añadir tu clave de OMDb:

OMDB_API_KEY = "TU_CLAVE"
OMDB_BASE_URL = "https://www.omdbapi.com/"

# Base de datos

Archivo: data/movies.sqlite

Tabla utilizada: comentarios
Campos:
- id
- id_pelicula
- persona
- comentario
- fecha

# Ejecución del programa

En Windows:
set FLASK_APP=main.py
flask run

En Mac:
export FLASK_APP=main.py
flask run

Modo debug:
flask run --debug

La aplicación se ejecuta en:
http://127.0.0.1:5000