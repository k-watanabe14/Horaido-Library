import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy import and_, or_


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
from app.models import Book, History, User, TagMaps, Tags


@app.errorhandler(404)
def not_found(error):

    return render_template('404.html'), 404


@app.route('/', methods=('GET', 'POST'))
@login_required
def index():

    new_books = Book.query.outerjoin(User, TagMaps, Tags).filter(or_(TagMaps.tag_id <= 9, TagMaps.tag_id == None)).add_columns(User.username, Tags.tag_name).order_by(Book.id.desc()).limit(10)

    rental_books = Book.query.join(History).outerjoin(User, TagMaps, Tags).filter(or_(TagMaps.tag_id <= 9, TagMaps.tag_id == None)).add_columns(User.username, Tags.tag_name).order_by(History.id.desc()).limit(10)

    if request.method == 'POST':
        keyword = request.form['keyword']
        error = None

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search', keyword=keyword))

    return render_template('index.html', new_books=new_books, rental_books=rental_books)


@app.route('/search', methods = ('GET', 'POST'))
@login_required
def search():

    tags = Tags.query

    keyword = request.args.get('keyword')
    status = request.args.get('status')
    tag = request.args.get('tag') if request.args.get('tag') else '-1'

    f_keyword = "%{}%".format(keyword)

    # Search books contained keyword in title, author, publisher name.
    keywords= or_((Book.title.like(f_keyword)), ((Book.author.like(f_keyword))), (Book.publisher_name.like(f_keyword)))

    # For pagination
    page = request.args.get('page', 1, type = int)

    status_condition = and_(True)
    if status == "loaned-out":
        status_condition = and_(Book.borrower_id != None)
    elif status == 'available':
        status_condition = and_(Book.borrower_id == None)

    tag_condition = and_(True)
    if tag != '-1':
        tag_condition = and_(TagMaps.tag_id == tag)

    # "results" are collections of books.
    # Display 20 results per a page.
    results = Book.query.outerjoin(User, TagMaps).filter(keywords, status_condition, tag_condition).add_columns(User.username).paginate(page = page, per_page = 20)

    if request.method == 'POST':
        keyword = request.form['keyword']
        status = request.form.get('status')
        tag = request.form.get('tag')
        return redirect(url_for('search', keyword=keyword, status=status, tag=tag))

    return render_template('search.html', results=results, keyword=keyword, status=status, tags=tags, tag=tag)

# ENHANCE: Send email before due date if not returning the book yet
@app.route('/rental')
@login_required
def rental():

    # SELECT *  FROM BOOK JOIN rental_history ON book.id = rental_history.book_id WHERE rental_history.user_id = user_id AND rental_history.return_date is NULL
    rental_books = Book.query.join(History).outerjoin(TagMaps, Tags).add_columns(Tags.tag_name).filter(Book.borrower_id == session.get('user_id'), or_(TagMaps.tag_id <= 9, TagMaps.tag_id == None))

    return render_template('rental.html', rental_books=rental_books)


if __name__ == '__main__':
    app.run()

# ENHANCE: Add a function to post reviews