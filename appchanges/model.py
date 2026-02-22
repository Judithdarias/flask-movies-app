import requests as consulta
from appchanges.config import OMDB_API_KEY, OMDB_BASE_URL

class ModelMovies:
    def __init__(self):
        self.url = ""
        self.response = None
        self.objeto_general = None

        # para la búsqueda
        self.title = None
        self.year = None
        self.results = []     # lista de películas (Search)
        self.message = None   # mensajes tipo "Movie not found!"

        # para el detalle
        self.imdb_id = None
        self.movie_detail = None

    def searchMovies(self, title, year=""):
        self.title = (title or "").strip()
        self.year = (year or "").strip()
        self.results = []
        self.message = None

        if self.title == "":
            raise Exception("El título es obligatorio")

        # Construimos la URL con params
        params = {
            "apikey": OMDB_API_KEY,
            "s": self.title,
            "type": "movie"
        }
        if self.year != "":
            params["y"] = self.year

        try:
            self.response = consulta.get(OMDB_BASE_URL, params=params, timeout=10)
        except Exception:
            raise Exception("Error conectando con OMDb")

        if self.response.status_code != 200:
            raise Exception("Error en consulta http")

        self.objeto_general = self.response.json()

        # OMDb usa Response: "False" cuando no hay resultados
        if self.objeto_general.get("Response") == "False":
            self.message = self.objeto_general.get("Error", "Sin resultados")
            self.results = []
            return

        self.results = self.objeto_general.get("Search", [])

    def getMovieDetail(self, imdb_id):
        self.imdb_id = (imdb_id or "").strip()
        self.movie_detail = None

        if self.imdb_id == "":
            raise Exception("imdb_id inválido")

        params = {
            "apikey": OMDB_API_KEY,
            "i": self.imdb_id,
            "plot": "full"
        }

        try:
            self.response = consulta.get(OMDB_BASE_URL, params=params, timeout=10)
        except Exception:
            raise Exception("Error conectando con OMDb")

        if self.response.status_code != 200:
            raise Exception("Error en consulta http")

        self.objeto_general = self.response.json()

        if self.objeto_general.get("Response") == "False":
            raise Exception(self.objeto_general.get("Error", "No encontrada"))

        self.movie_detail = self.objeto_general