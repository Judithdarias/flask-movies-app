from flask import render_template, request, redirect
from appchanges.model import *

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
            comentarios = select_comentarios_por_pelicula(imdb_id)
            return render_template("detail.html", movie=model.movie_detail, comentarios=comentarios)
        except Exception as e:
            return render_template("error.html", message=str(e))

    @app.post("/movie/<imdb_id>/comentario")
    def guardar_comentario(imdb_id):
        persona = request.form.get("persona", "")
        comentario = request.form.get("comentario", "")

        if persona == "" or comentario == "":
            return render_template("error.html", message="Nombre y comentario son obligatorios")

        try:
            insert_comentario(imdb_id, persona, comentario)
            return redirect(f"/movie/{imdb_id}")
        except Exception as e:
            return render_template("error.html", message=str(e))