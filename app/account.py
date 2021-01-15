from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth import login_required
from app import db, mail, app
from app.forms import RequestResetForm, ResetPasswordForm
from app.models import User
from flask_mail import Message
from werkzeug.security import generate_password_hash

# Define the blueprint: 'register', set its url prefix: app.url/register
mod_account = Blueprint('account', __name__, url_prefix='/account')

# TODO: Implement account setting
@mod_account.route('/')
@login_required
def index():
    return render_template('account/index.html')


@mod_account.route('/request_reset_password/', methods=('GET', 'POST'))
def request_reset_password():

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email_for_reset(user)
        flash('パスワード再設定のメールを送りました。')
        return redirect(url_for('auth.login'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)

    return render_template('account/request_reset_password.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    user = User.verify_reset_token(token)

    if user is None:
        flash('無効のURLです。', 'warning')
        return redirect(url_for('account.request_reset_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('パスワードを再設定しました。', 'success')

        return redirect(url_for('auth.login'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)

    return render_template('account/reset_password.html', form=form)


def send_email_for_reset(user):

    token = user.get_reset_token()

    msg = Message('パスワード再設定', sender="朋来堂ライブラリー", recipients=[user.email])

    msg.body = '''パスワードの再設定がリクエストされました。リンク先からパスワードを再設定してください。\r\n {url} \r\n \r\n パスワードを変更する必要がない場合は、何もする必要はありません。'''.format(url=url_for('reset_password', token=token, _external=True))

    mail.send(msg)