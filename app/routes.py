from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import true
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, CreateEventsForm
from flask_login import current_user, login_user
from app.models import User, Event
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm




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
        if user is None or not user.check_password(form.password.data):  # if the username is found it checks the password
            flash('Invalid username or password')  # if either is wrong, message is flashed
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)  # activates User Login function used to remember that user is logged on
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


@app.route('/events')
def events():
    return render_template('events.html', title='Home')


@app.route('/studentHours')
def studentHours():
    return render_template('studentHours.html', title='Home')


@app.route('/TeacherIndex')
def TeacherIndex():
    return render_template('TeacherIndex.html', title='Home')


@app.route('/host')
def host():
    return render_template('host.html', title='Home')


@app.route('/eventSignup')
def eventSignup():
    return render_template('eventSignup.html', title='Home')


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


@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    form = CreateEventsForm()
    if form.validate_on_submit():
        event = Event(event_name=form.eventName.data, description=form.description.data, date=form.date.data)
        db.session.add(event)
        db.session.commit()
        flash('Congratulations, you have created a new event!')
        return redirect(url_for('events'))
    return render_template('createEvent.html', title='Create_Event', form=form)
