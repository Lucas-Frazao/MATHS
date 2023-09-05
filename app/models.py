# This file defines the User and Post functionalities of the application

from sqlalchemy import true, false
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin  # includes generic implementations that are appropriate for most user model classes
from app import login  # Flask-Login user loader function
from datetime import datetime

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model): # this is the user functionality, a user has an id, a username, an email, a password hash (Hashing a password means that it is encrypted) a level (teacher, student, host), and the relationship between it and posts: here, a user can
    # write a post and own it. Finally, it defines the rest of the followed function.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    level = db.Column(db.String(120), index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # methods bellow are for password hashing
    def set_password(self, password):  # This sets the password hash to a password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # this checks the password hash against a provided password to see if there is a match
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user): # This is the last piece of code that defines the unfollow functionality, it calls upon the user and orients it to 'unfollow' another user
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user): # This compares user ids to see if one user follows another user
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self): # This returns all posts that are written by people who you follow
        followed = Post.query.filter_by(user_id=self.id)
        return followed.order_by(Post.timestamp.desc())


@login.user_loader  # method gives an id that Flask-Login uses to keep track of User session status
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model): # This defines the posts that will be written by the user, eventually, 'posts' will be morphed into events for members to go to. The follow and unfollow functions will be morphed into attended and did not attend functionalities.
    id = db.Column(db.Integer, primary_key=True) # The post class has four variables that define it: id, body, timestamp and user id.
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
