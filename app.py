from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from dotenv import load_dotenv
from models import db, Movie
import requests
import os
from werkzeug.exceptions import HTTPException

load_dotenv()
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'data/movies.db')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{file_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
db.init_app(app)

data_manager = DataManager()

@app.route('/')
def index():
    """Home page: show all users and form to add new user"""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user and add in the database"""
    user = request.form.get('username').strip()

    if not user:
        flash("Please enter a username.")
        return redirect(url_for('index'))

    data_manager.create_user(name=user)
    flash("User created successfully.")
    return redirect(url_for('index'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Retrieves the user’s list of favorite movies and displays it."""
    user = data_manager.get_user_by_id(user_id)

    if user is None:
        flash(f"User with ID {user_id} not found")
        return redirect(url_for('index'))

    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user=user)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_favourite_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    movie_title = request.form.get('movie_title')
    if not movie_title:
        flash("Please enter a movie title")
        return redirect(url_for('user_movies', user_id=user_id))

    # Fetch data from OMDb API
    url = f'https://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'False' or response.status_code != 200:
        flash(f"Movie '{movie_title}' not found!")
        return redirect(url_for('user_movies', user_id=user_id))

    new_movie = Movie(
        name=data.get("Title"),
        director=data.get("Director"),
        year=data.get("Year"),
        poster_url=data.get("Poster"),
        user_id=user_id
    )

    data_manager.add_movie(new_movie)
    flash(f"Movie '{movie_title}' successfully added", 'success')
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """ Modify the title of a specific movie in a user’s list"""
    new_title = request.form.get('new_title')
    if not new_title or len(new_title) == 0:
        flash("Please enter a movie title")

    updated_movie = data_manager.update_movie(movie_id, new_title)

    if updated_movie is None:
        flash(f"Movie '{new_title}' not found!")
        return redirect(url_for('user_movies', user_id=user_id))

    flash(f"Movie '{new_title}' successfully updated", 'success')
    return redirect(url_for('user_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    deleted_movie = data_manager.delete_movie(movie_id)

    if deleted_movie is None:
        flash(f"Movie '{movie_id}' not found")
        return redirect(url_for('user_movies', user_id=user_id))

    flash(f"Movie  successfully deleted", 'success')
    return redirect(url_for('user_movies', user_id=user_id))




@app.errorhandler(Exception)
def handle_error(e):
    """Handles all exceptions and renders a generic error page."""
    if isinstance(e, HTTPException):
        error_code = e.code
    else:
        error_code = 500
    return render_template('error.html', error_code=error_code), error_code




if __name__ == '__main__':
    with app.app_context():
         db.create_all()
         print(f"Database created successfully at: {file_path}")
    app.run(host='0.0.0.0',port=5000, debug=True)


