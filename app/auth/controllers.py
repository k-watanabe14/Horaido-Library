from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from app.auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    flash('Wrong email or password', 'error-message')

    return render_template("auth/signup.html")


@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    flash('Wrong email or password', 'error-message')

    return render_template("auth/login.html")