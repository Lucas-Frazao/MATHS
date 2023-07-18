from sqlalchemy import true, false
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin  # includes generic implementations that are appropriate for most user model classes
from app import login  # Flask-Login user loader function


class User  (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    level = db.Column(db.String(120), index=True)
    events = db.relationship('Event', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # methods bellow are for password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader  # method gives an id that Flask-Login uses to keep track of User session status
def load_user(id):
    return User.query.get(int(id))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64))
    description = db.Column(db.String(140))
    date = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Event {}>'.format(self.description)
