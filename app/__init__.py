# this is the file that MATHS.py imports to initiate the program, also, MATHS.py is the first file that the cmd runs to initiate the program
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # makes sure user is logged in before visiting other parts of the application
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

# The script above simply creates the application object as an instance of
# class Flask imported from the flask package.
