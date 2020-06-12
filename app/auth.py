import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db
 
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/')


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.session.query(User).filter(User.username == username).count() != 0:
            error = 'User {} is already registered.'.format(username)
        elif db.session.query(User).filter(User.email == email).count() != 0:
            error = 'Email {} is already registered.'.format(email)


        if error is None:
            data = User(username, email, generate_password_hash(password))
            db.session.add(data)
            db.session.commit()
            flash('ユーザーを登録しました')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template("auth/signup.html")


@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = db.session.query(User).filter(User.username == username).first()
        print(user)

        if user is None:
            error = 'ユーザ名が間違っています。.'
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
        g.user = db.session.query(User).filter(User.id == user_id).first()


@mod_auth.route('/logout')
def logout():

    session.clear()
    flash('ログアウトしました')
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
