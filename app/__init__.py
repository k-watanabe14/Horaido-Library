import os
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Import a module / component using its blueprint handler
from app.auth import mod_auth
from app.account import mod_account
from app.search import mod_search
from app.register import mod_register
from app.book import mod_book

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_account)
app.register_blueprint(mod_search)
app.register_blueprint(mod_register)
app.register_blueprint(mod_book)

# Import login_required
from app.auth import login_required

#Import Book Model
from app.models import Book, History


@app.errorhandler(404)
def not_found(error):

    return render_template('404.html'), 404


@app.route('/')
@login_required
def index():

    new_books = db.session.query(Book).order_by(Book.id.desc()).limit(10)
    
    return render_template('index.html', new_books = new_books)


@app.route('/borrow', methods=('GET', 'POST'))
@login_required
def borrow():

    if request.method == 'POST':
        isbn = request.form['isbn']
        error = None

        if not isbn:
            error = 'isbn is required.'

        if error is not None:
            flash(error)
        else:
            book = db.session.query(Book).filter(Book.isbn == isbn).first()
            return redirect(url_for('book.borrow', book_id=book.id))

    return render_template('borrow.html')


@app.route('/return', methods=('GET', 'POST'))
@login_required
def return_():
    
    # SELECT *  FROM book JOIN rental_history ON book.id = rental_history.book_id WHERE rental_history.user_id = user_id AND rental_history.return_date is NULL
    rental_books = db.session.query(Book).join(History, Book.id==History.book_id).filter(History.user_id == session.get('user_id'),  History.return_date == None)

    return render_template('return.html', rental_books = rental_books)


if __name__ == '__main__':
    app.run()
