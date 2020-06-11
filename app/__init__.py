import os
from flask import Flask, render_template, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.auth.views import login_required
from app.models import Book

mod_index = Blueprint('index', __name__, url_prefix='/')

@mod_index.route('/')
@login_required
def index():
    newbooks = db.session.query(Book).order_by(Book.id.desc()).limit(10)
    return render_template('index.html', newbooks = newbooks)


@mod_borrow.route('/borrow')
@login_required
def index():

    if request.method == 'POST' and isbn is None:
        isbn = request.form['isbn']
        error = None

        if not isbn:
            error = 'isbn is required.'

        if error is not None:
            flash(error)
        else:
            book = db.session.query(Book).filter(Book.isbn == isbn).first()
            return redirect(url_for('book.isbn', book=book)

    return render_template('borrow.html')


@mod_return.route('/')
@login_required
def index():
    return render_template('return/index.html')


# Import a module / component using its blueprint handler
from app.auth.views import mod_auth
from app.account.views import mod_account
from app.search.views import mod_search
from app.register.views import mod_register
from app.borrow.views import mod_borrow
from app.return_.views import mod_return

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_account)
app.register_blueprint(mod_search)
app.register_blueprint(mod_register)
app.register_blueprint(mod_borrow)
app.register_blueprint(mod_return)


if __name__ == '__main__':
    app.run()
