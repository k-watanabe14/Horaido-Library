from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth.controllers import login_required
from app.auth.models import Book
from app import db
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_register = Blueprint('register', __name__, url_prefix='/register')


@mod_register.route('/auto', methods=('GET', 'POST'))
@login_required
def auto():
    if request.method == 'POST':
        isbn = request.form['isbn']
        error = None

        if not isbn:
            error = 'isbn is required.'

        if error is not None:
            flash(error)
        else:
            url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?applicationId=1053085901834686387&isbn=' + isb

            return redirect(url_for('register.confirm'))

    return render_template('register/auto.html')


@mod_register.route('confirm', method=('GET'))
@login_required
def confirm(isbn):

    