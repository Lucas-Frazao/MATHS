from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import true
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Post
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
from app.forms import PostForm
from app.forms import EmptyForm
from datetime import datetime
from app.forms import EditProfileForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # if user is logged in already
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # finds the user based on username
        if user is None or not user.check_password(
                form.password.data):  # if the username is found it checks the password
            flash('Invalid username or password')  # if either is wrong, message is flashed
            return redirect(url_for('login'))
        login_user(user,
                   remember=form.remember_me.data)  # activates User Login function used to remember that user is logged on
        holder = " "
        if user.level == "student":
            holder = url_for('index')
        elif user.level == "teacher":
            holder = url_for('TeacherIndex')
        elif user.level == "host":
            holder = url_for('host')
        else:
            holder = url_for('login')
        return redirect(holder)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/scanEvent')
def scanEvent():
    return render_template('scanEvent.html', title='Home')


@app.route('/studentHours')
def studentHours():
    return render_template('studentHours.html', title='Home')


@app.route('/TeacherIndex')
def TeacherIndex():
    return render_template('TeacherIndex.html', title='Home')


@app.route('/host')
def host():
    return render_template('host.html', title='Home')


@app.route('/serviceHours')
def serviceHours():
    return render_template('serviceHours.html', title='Home')


@app.route('/troubleLogin')
def troubleLogin():
    return render_template('troubleLogin.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])  # User registration view function
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, level=form.level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/createEvent', methods=['GET', 'POST'])
@login_required
def createEvent():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('TeacherIndex'))
    posts = current_user.followed_posts().all()
    return render_template("createEvent.html", title='Home Page', form=form, posts=posts)


@app.route('/events', methods=['GET', 'POST'])
def events():
    posts = current_user.followed_posts().all()
    return render_template("events.html", title='Home Page', posts=posts)


@app.route('/eventSignup', methods=['GET', 'POST'])
def eventSignup():
    posts = current_user.followed_posts().all()
    return render_template("eventSignup.html", title='Home Page', posts=posts)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
