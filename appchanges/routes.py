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

            promedio = model.obtener_promedio(imdb_id)

            return render_template(
                "detail.html",
                movie=model.movie_detail,
                comentarios=comentarios,
                promedio=promedio
            )
        except Exception as e:
            return render_template("error.html", message=str(e))
    @app.post("/movie/<imdb_id>/feedback")
    def guardar_feedback(imdb_id):
        persona = request.form.get("persona", "").strip()
        comentario = request.form.get("comentario", "").strip()
        puntuacion = request.form.get("puntuacion", "").strip()

        if persona == "":
            return render_template("error.html", message="El nombre es obligatorio")

        # si no envía nada (ni comentario ni puntuación)
        if comentario == "" and puntuacion == "":
            return render_template("error.html", message="Escribe un comentario o selecciona una puntuación")

        # guardar comentario si viene
        if comentario != "":
            insert_comentario(imdb_id, persona, comentario)

        # guardar puntuación si viene
        if puntuacion != "":
            try:
                puntuacion_int = int(puntuacion)
            except:
                return render_template("error.html", message="Puntuación inválida")

            if puntuacion_int < 1 or puntuacion_int > 5:
                return render_template("error.html", message="La puntuación debe estar entre 1 y 5")

            model.insert_calificacion(imdb_id, persona, puntuacion_int)

        return redirect(f"/movie/{imdb_id}")
        
    @app.get("/movie/<imdb_id>/calificar/<int:puntuacion>")
    def calificar(imdb_id, puntuacion):

        if puntuacion < 1 or puntuacion > 5:
            return render_template("error.html", message="Puntuación inválida")

        model.insert_calificacion(imdb_id, puntuacion)
        return redirect(f"/movie/{imdb_id}")
    
