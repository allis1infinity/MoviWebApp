from flask import Flask
from data_manager import DataManager
from dotenv import load_dotenv
from models import db, Movie
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'data/movies.db')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{file_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print(f"Database created successfully at: {file_path}")
    app.run(host='0.0.0.0',port=5000, debug=True)


