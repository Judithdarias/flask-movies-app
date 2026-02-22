from flask import render_template, request
from appchanges.model import ModelMovies

model = ModelMovies()

def register_routes(app):

    @app.get("/")
    def home():
        return render_template("search.html")

    @app.get("/search")
    def search():
        title = request.args.get("title", "")
        year = request.args.get("year", "")

        try:
            model.searchMovies(title, year)
            return render_template("results.html", results=model.results, message=model.message)
        except Exception as e:
            return render_template("error.html", message=str(e))
        
    @app.get("/movie/<imdb_id>")
    def movie_detail(imdb_id):
        try:
            model.getMovieDetail(imdb_id)
            return render_template("detail.html", movie=model.movie_detail)
        except Exception as e:
            return render_template("error.html", message=str(e))