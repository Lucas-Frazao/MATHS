# The following file provides the routes for all the URLs of the pages in the application

# The code below imports all necessary supporting code
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


# The code below routes the index page for the students
@app.route('/')
@app.route('/index')
@login_required  # This means that a user must login before accesing this route
def index():
    return render_template('index.html', title='Home')


# The code below routes the login page for all users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # if the user is logged in already then there is no reason for them to login again, thus, they will be redirected to their assigned index - On a side note, I have to fix the code below because right now it redirects ANY user
        return redirect(url_for('index'))  # to the student index
    form = LoginForm()  # this assigns the variable form to hold the login form
    if form.validate_on_submit():  # if the information goes through properly when the user clicks the submit button then...
        user = User.query.filter_by(username=form.username.data).first()  # finds the user based on username
        if user is None or not user.check_password(
                form.password.data):  # if the username is found it checks the password
            flash('Invalid username or password')  # if either is wrong, message is flashed
            return redirect(url_for('login'))
        login_user(user,
                   remember=form.remember_me.data)  # activates User Login function used to remember that user is logged on
        # The code below redirects the user based on his level
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


@app.route('/logout')  # This routes the logout button and points a user back to the login page
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/scanEvent')  # This routes the scanEvent page
def scanEvent():
    return render_template('scanEvent.html', title='Home')


@app.route('/studentHours')  # This routes the studentHours page
def studentHours():
    return render_template('studentHours.html', title='Home')


@app.route('/TeacherIndex')  # This routes the TeacherIndex page
def TeacherIndex():
    return render_template('TeacherIndex.html', title='Home')


@app.route('/host')  # This routes the host page
def host():
    return render_template('host.html', title='Home')


@app.route('/serviceHours')  # This routes the serviceHours page
def serviceHours():
    return render_template('serviceHours.html', title='Home')


@app.route('/troubleLogin')  # This routes the troubleLogin page
def troubleLogin():
    return render_template('troubleLogin.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])  # Routes the register page
def register():
    if current_user.is_authenticated:  # if the user is logged in already then there is no reason why he should be able to register, thus he will be redirected to the index page. On a side note, I have to fix the redirect because right now it pints ANY user to the
        # student homepage.
        return redirect(url_for('index'))
    form = RegistrationForm()  # assigns the variable form to the registration form
    if form.validate_on_submit():  # if all information goes through properly when the user hits the submit button then...
        user = User(username=form.username.data, email=form.email.data,
                    level=form.level.data)  # gives the user's username, email and level variables the data retrieved from the form (form.username.data, form.email.data, form.level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  # the previous three lines of code commit the data retrieved from the web form to the SQL-lite database
        flash('Congratulations, you are now a registered user!')
        return redirect(
            url_for('login'))  # sends the user back to the login so he can login using his newly-created account
    return render_template('register.html', title='Register', form=form)


@app.route('/', methods=['GET', 'POST'])  # defines the method of communication as get and post.
@app.route('/createEvent', methods=['GET', 'POST'])  # routes the createEvent page
@login_required  # requires login
def createEvent():
    form = PostForm()  # sets form equal to post form
    if form.validate_on_submit():  # if all information is valid upon submit then...
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit() # the above three lines get all data from the forms and commit it to the database
        flash('Your post is now live!')  # message that lets user know their post is now live
        return redirect(url_for('events'))  # user is sent back to the teacher index, in this case only teachers can create events so their is no need to route the user back to any other homepage except for the teacher homepage
    posts = current_user.followed_posts().all()  # gets all posts written by people the user follows
    return render_template("createEvent.html", title='Home Page', form=form, posts=posts)


@app.route('/events', methods=['GET', 'POST'])  # defines get post as communication method and routes events
def events():
    posts = current_user.followed_posts().all()  # returns all posts written by people who the user follows
    return render_template("events.html", title='Home Page', posts=posts)


@app.route('/eventSignup', methods=['GET', 'POST'])  # defines get post as communication and routes event signup
def eventSignup():
    posts = current_user.followed_posts().all()  # returns all posts written by people who the user follows
    return render_template("eventSignup.html", title='Home Page', posts=posts)


@app.route('/follow/<username>', methods=['POST']) # defines post as the method of communication and routes the follow function
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():  # if the form delivers all data properly then...
        user = User.query.filter_by(username=username).first()  # filters by username given
        if user is None:
            flash('User {} not found.'.format(username))  # if user is not found...
            return redirect(url_for('index'))  # sends user back to index
        if user == current_user:
            flash('You cannot follow yourself!')  # prevents people from following themselves
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()  # follows a user
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])  # routes the unfollow function and sets the communication to post method only
@login_required  # must have logged in to unfollow someone
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():  # if form submits proper data
        user = User.query.filter_by(username=username).first()  # filters user by username
        if user is None:  # if username is not found then...
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:  # prevents user from following themselves
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)  # unfollows user and commits it
        db.session.commit()
        flash('You are not following {}.'.format(username))  # tells user who they just followed
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))  # redirect to index


@app.route('/user/<username>')  # routes the username function
@login_required  # requires a login
def user(username):
    user = User.query.filter_by(username=username).first_or_404()  # filters by username
    posts = [  # defines post's structure
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


@app.route('/edit_profile', methods=['GET', 'POST'])  # routes the edit profile page and define communication as get post
@login_required  # requires a login
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():  # if form is properly submitted
        current_user.username = form.username.data  # sets the username to the username from the form
        current_user.about_me = form.about_me.data  # sets the user's about me to the about me from the form
        db.session.commit()  # commits data to database
        flash('Your changes have been saved.')  # tells users that their information has been saved
        return redirect(url_for('edit_profile'))  # goes back to the edit profile page
    elif request.method == 'GET':  # sets the request method to get
        form.username.data = current_user.username  # sets the username data to the current username
        form.about_me.data = current_user.about_me  # sets the about me data to the current about me.
    return render_template('edit_profile.html', title='Edit Profile', form=form)
