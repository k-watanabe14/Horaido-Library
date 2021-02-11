from flask import render_template, flash, session, redirect, url_for
from flask import g, Blueprint, request
from werkzeug.security import check_password_hash
from app.models import User
from app import app
from app.common import display_errors
import functools

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/')


@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    from app.forms import LoginFrom

    form = LoginFrom()

    username = form.username.data
    password = form.password.data

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                flash('ユーザー名もしくはパスワードが間違っています。', 'warning')
                app.logger.info(
                    '%s input wrong username or password', username)

            else:
                session.clear()
                session['user_id'] = user.id
                app.logger.info('%s logged in successfully', username)
                return redirect(url_for('index'))

        else:
            display_errors(form.errors.items)
            app.logger.info('%s failed to login', username)

    return render_template('auth/login.html', form=form)


@mod_auth.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


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
