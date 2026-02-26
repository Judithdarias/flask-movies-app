import requests as consulta
from appchanges.config import OMDB_API_KEY, OMDB_BASE_URL
import sqlite3
from datetime import datetime

class ModelMovies:
    def __init__(self):
        self.results = []
        self.message = None
        self.movie_detail = None

    def searchMovies(self, title, year=""):
        title = (title or "").strip()
        year = (year or "").strip()

        if title == "":
            raise Exception("El título es obligatorio")

        params = {"apikey": OMDB_API_KEY, "s": title, "type": "movie"}
        if year:
            params["y"] = year

        response = consulta.get(OMDB_BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code} - {response.text}")

        data = response.json()

        if data.get("Response") == "False":
            self.message = data.get("Error", "Sin resultados")
            self.results = []
            return

        self.message = None
        self.results = data.get("Search", [])

    def getMovieDetail(self, imdb_id):

        datos_peticion = {
            "apikey": OMDB_API_KEY,
            "i": imdb_id,
            "plot": "full"
    }

        respuesta = consulta.get(OMDB_BASE_URL, params=datos_peticion, timeout=10)

        if respuesta.status_code != 200:
            raise Exception("Error en consulta http")

        datos = respuesta.json()

        if datos.get("Response") == "False":
            raise Exception(datos.get("Error", "No encontrada"))

        self.movie_detail = datos

    def obtener_promedio(self, id_pelicula):

        conn = sqlite3.connect("data/movies.sqlite")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT AVG(puntuacion) FROM Calificaciones WHERE id_pelicula = ?",
            (id_pelicula,)
        )

        resultado = cursor.fetchone()
        conn.close()

        if resultado[0] is None:
            return 0

        return round(resultado[0], 1)
    
    def insert_calificacion(self, id_pelicula, persona, puntuacion):

        conn = sqlite3.connect("data/movies.sqlite")
        cursor = conn.cursor()

        fecha = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO Calificaciones (id_pelicula, persona, puntuacion, fecha) VALUES (?,?,?,?)",
            (id_pelicula, persona, puntuacion, fecha)
        )

        conn.commit()
        conn.close()

def insert_comentario(id_pelicula, persona, comentario):

    conn = sqlite3.connect("data/movies.sqlite")
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO comentarios (id_pelicula, persona, comentario, fecha) VALUES (?,?,?,?)",
        (id_pelicula, persona, comentario, fecha)
    )

    conn.commit()
    conn.close()

def select_comentarios_por_pelicula(id_pelicula):

    conn = sqlite3.connect("data/movies.sqlite")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT persona, comentario, fecha FROM comentarios WHERE id_pelicula = ? ORDER BY id DESC",
        (id_pelicula,)
    )

    filas = cursor.fetchall()
    conn.close()

    lista = []
    for f in filas:
        lista.append(dict(f))

    return lista

    

    