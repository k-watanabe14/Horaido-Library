from flask import render_template, Blueprint, request, flash, redirect, url_for
from app import app, db
from app.auth import login_required
from app.models import User
from app.common import display_errors
from werkzeug.security import generate_password_hash

# Define the blueprint: 'register', set its url prefix: app.url/register
mod_users = Blueprint('users', __name__, url_prefix='/users')


@mod_users.route('/')
@login_required
def index():

    users = User.query.order_by(User.id.asc())

    return render_template('users/index.html', users=users)


@mod_users.route('/create', methods=('GET', 'POST'))
@login_required
def register():
    from app.forms import UserForm

    form = UserForm()

    username = form.username.data
    email = form.email.data
    password = form.password.data
    admin = False

    if request.method == 'POST':
        if form.validate_on_submit():

            user = User(username, email, generate_password_hash(password),
                        admin)
            db.session.add(user)
            db.session.commit()

            flash('ユーザーを登録しました')
            app.logger.info('Registered a new account successfully')
            return redirect(url_for('users.index'))

        else:
            display_errors(form.errors.items)
            app.logger.info('Failed to register a new account')

    return render_template('users/register.html', form=form)
