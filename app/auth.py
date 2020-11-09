import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db, mail
from app.forms import SignupForm 

 
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/')


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm()  

    if request.method == 'POST':

        username = form.username.data
        email = form.email.data
        password = form.password.data
        error = None

        if User.query.filter_by(username=username).count() != 0:
            error = 'User {} is already registered.'.format(username)
        elif User.query.filter_by(email=email).count() != 0:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            user = User(username, email, generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

            # Automatically login
            session.clear()
            session['user_id'] = User.query.filter_by(username=username).first().id

            flash('ユーザーを登録しました')
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/signup.html", form=form)


@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'ユーザ名もしくはパスワードが間違っています。'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@mod_auth.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@mod_auth.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
