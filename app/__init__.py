from flask import Flask
from flask_migrate import Migrate  # database
from flask_sqlalchemy import SQLAlchemy  # database

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# The script above simply creates the application object as an instance of
# class Flask imported from the flask package.
