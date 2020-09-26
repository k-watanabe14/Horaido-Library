import os
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
mail = Mail(app)


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

    rental_books = db.session.query(Book).join(History, Book.id == History.book_id).order_by(History.id.desc()).limit(10)

    if request.method == 'POST':
        keyword = request.form['keyword']
        error = None

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search', keyword=keyword))
    
    return render_template('index.html', new_books = new_books, rental_books = rental_books)


@app.route('/search', methods = ('GET', 'POST'))
def search():
    
    keyword = request.args.get('keyword')
    status = request.args.get('status')
    genre = request.args.get('genre')
    donor = request.args.get('donor')

    search_keyword = "%{}%".format(keyword)
    search_status = "%{}%".format(status)
    search_genre = "%{}%".format(genre)
    search_donor = "%{}%".format(donor)

    # Search books contained keyword in title, author, publisher name.
    keyword_condition = or_((Book.title.like(search_keyword)), ((Book.author.like(search_keyword))), (Book.publisher_name.like(search_keyword)))

    # Book status

    # Book genre

    # For pagination
    page = request.args.get('page', 1, type = int)  

    # "results" are collections of books.
    # Display 20 results per a page.
    if status == "loaned-out":
        results = Book.query.filter(keyword_condition, Book.borrower_id != None).paginate(page = page, per_page = 20)
    elif status == 'available':
        results = Book.query.filter(keyword_condition, Book.borrower_id == None).paginate(page = page, per_page = 20)
    else:
        results = Book.query.filter(keyword_condition).paginate(page = page, per_page = 20)

    if request.method == 'POST':
        keyword = request.form['keyword']
        status = request.form.get('status')
        genre = request.form.get('genre')
        donor = request.form.get('donor')
        error = None

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search', keyword = keyword, status = status, genre = genre, donor = donor))

    return render_template('search.html', results = results, keyword = keyword, status = status, genre = genre, donor = donor)


@app.route('/return')
@login_required
def return_():
    
    # SELECT *  FROM book JOIN rental_history ON book.id = rental_history.book_id WHERE rental_history.user_id = user_id AND rental_history.return_date is NULL
    rental_books = db.session.query(Book).join(History, Book.id==History.book_id).filter(History.user_id == session.get('user_id'),  History.return_date == None)

    return render_template('return.html', rental_books = rental_books)


if __name__ == '__main__':
    app.run()
