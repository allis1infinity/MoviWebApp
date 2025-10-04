from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'



class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Movie {self.name}>'


#users_movies = db.Table('users_movies',
#                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#                  db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')))



