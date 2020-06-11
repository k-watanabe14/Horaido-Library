import os
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.auth import login_required
from app.models import Book


@app.route('/')
@login_required
def index():
    newbooks = db.session.query(Book).order_by(Book.id.desc()).limit(10)
    return render_template('index.html', newbooks = newbooks)


@app.route('/borrow')
@login_required
def borrow():

    if request.method == 'POST' and isbn is None:
        isbn = request.form['isbn']
        error = None

        if not isbn:
            error = 'isbn is required.'

        if error is not None:
            flash(error)
        else:
            book = db.session.query(Book).filter(Book.isbn == isbn).first()
            return redirect(url_for('book.isbn', book=book))

    return render_template('borrow.html')


@app.route('/return')
@login_required
def return_():
    return render_template('return.html')


# Import a module / component using its blueprint handler
from app.auth import mod_auth
from app.account import mod_account
from app.search import mod_search
from app.register import mod_register

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_account)
app.register_blueprint(mod_search)
app.register_blueprint(mod_register)


if __name__ == '__main__':
    app.run()
