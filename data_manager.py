from models import db, User, Movie

class DataManager:
    # Define Crud operations as methods

    def create_user(self, name):
        """Add a new user to the User table"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user


    def get_users(self):
        """Returns a list of all User objects."""
        users =  User.query.all()
        return users


    def get_movies(self, user_id):
        """ Returns a list of all movies of a specific user."""
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies


    def add_movie(self, movie):
        """Add a new movie to the Movie table"""
        db.session.add(movie)
        db.session.commit()
        return movie


    def update_movie(self, movie_id, new_title):
        """Update the details of a specific movie in the database."""
        movie = Movie.query.get(movie_id)

        if movie:
            movie.name = new_title
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
         """Delete the movie from the user’s list of favorites."""
         movie = Movie.query.get(movie_id)
         if movie:
             db.session.delete(movie)
             db.session.commit()
             return movie
         return None









