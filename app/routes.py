from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)