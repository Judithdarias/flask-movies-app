import requests as consulta
from appchanges.config import OMDB_API_KEY, OMDB_BASE_URL

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


        