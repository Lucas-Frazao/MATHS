from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
# The script above simply creates the application object as an instance of
# class Flask imported from the flask package.


