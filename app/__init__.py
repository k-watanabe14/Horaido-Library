import os
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)


# Import a module / component using its blueprint handler
from app.auth import mod_auth
from app.account import mod_account
from app.register import mod_register
from app.book import mod_book

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_account)
app.register_blueprint(mod_register)
app.register_blueprint(mod_book)

# Import login_required
from app.auth import login_required

# Import Book Model
from app.models import Book, History, User


@app.errorhandler(404)
def not_found(error):

    return render_template('404.html'), 404


@app.route('/', methods=('GET', 'POST'))
@login_required
def index():

    new_books = db.session.query(Book).order_by(Book.id.desc()).limit(10)

    rental_books = db.session.query(Book, History, User).join(History, Book.id == History.book_id).join(User, History.user_id == User.id).order_by(History.id.desc()).limit(10)

    if request.method == 'POST':
        keyword = request.form['keyword']
        error = None

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search', keyword=keyword))
    
    return render_template('index.html', new_books = new_books, rental_books = rental_books)


@app.route('/borrow', methods = ('GET', 'POST'))
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
            return redirect(url_for('book.borrow', book = book))

    return render_template('borrow.html')


@app.route('/return')
@login_required
def return_():
    
    # SELECT *  FROM book JOIN rental_history ON book.id = rental_history.book_id WHERE rental_history.user_id = user_id AND rental_history.return_date is NULL
    rental_books = db.session.query(Book).join(History, Book.id==History.book_id).filter(History.user_id == session.get('user_id'),  History.return_date == None)

    return render_template('return.html', rental_books = rental_books)


@app.route('/search', methods = ('GET', 'POST'))
@login_required
def search():
    
    keyword = request.args.get('keyword')
    
    search_keyword = "%{}%".format(keyword)

    # Search books contained keyword in title, author, publisher name.
    # results are collections of books.
    results = Book.query.filter(or_((Book.title.like(search_keyword)), ((Book.author.like(search_keyword))), (Book.publisher_name.like(search_keyword)))).all()

    print(results)

    if request.method == 'POST':
        keyword = request.form['keyword']
        error = None

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search', keyword = keyword))

    return render_template('search.html', results = results)


if __name__ == '__main__':
    app.run()
