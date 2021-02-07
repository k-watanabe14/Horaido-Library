from flask import render_template, flash, redirect, url_for, Blueprint
from app.auth import login_required
from app import app, db, mail
from app.forms import RequestResetForm, ResetPasswordForm
from app.models import User
from flask_mail import Message
from werkzeug.security import generate_password_hash
from app.common import display_errors

# Define the blueprint: 'register', set its url prefix: app.url/register
mod_account = Blueprint('account', __name__, url_prefix='/account')


# ENHANCE: Implement account setting
@mod_account.route('/')
@login_required
def index():
    return render_template('account/index.html')


@mod_account.route('/request_reset_password/', methods=('GET', 'POST'))
def request_reset_password():

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_email_for_reset(user)
            flash('パスワード再設定のメールを送りました。30分以内にパスワードを再設定してください。')
            app.logger.info('%s requested password reset', user.username)
        except Exception as e:
            flash('エラーが発生しました。時間をおいてから再度試してください。', 'warning')
            app.logger.exception(
                '%s could not get a password reset mail: %s', user.username, e)
        return redirect(url_for('auth.login'))

    else:
        display_errors(form.errors.items)

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
        app.logger.info('%s reset password successfully', user.username)
        flash('パスワードを再設定しました。')

        return redirect(url_for('auth.login'))

    else:
        display_errors(form.errors.items)

    return render_template('account/reset_password.html', form=form)


def send_email_for_reset(user):

    token = user.get_reset_token()

    msg = Message('パスワード再設定', sender='朋来堂ライブラリー', recipients=[user.email])

    msg.body = 'パスワードの再設定がリクエストされました。30分以内にリンク先からパスワードを再設定してください。\r\n {url}\
        \r\n\r\n パスワードを変更する必要がない場合は、何もする必要はありません。'.format(
        url=url_for('reset_password', token=token, _external=True))

    mail.send(msg)
