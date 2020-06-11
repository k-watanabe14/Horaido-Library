from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth import login_required
from app.models import Book, History
from app import db
from app.auth import load_logged_in_user
import datetime
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_book = Blueprint('book', __name__, url_prefix='/book')


@mod_book.route('/')
@login_required
def index():
    return render_template('book/index.html')


@mod_book.route('/<int:book_id>/borrow', methods=('GET', 'POST'))
@login_required
def borrow(book_id):

    book = db.session.query(Book).filter(Book.id == book_id).first()

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            user_id = session.get('user_id')
            checkout_date = datetime.datetime.today().strftime('%Y/%m/%d')
            due_date = None
            return_date = None

            data = History(book_id, user_id, checkout_date, due_date, return_date)
            db.session.add(data)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('book/borrow.html', book=book)


@mod_book.route('/<int:book_id>/return', methods=('GET', 'POST'))
@login_required
def return_(book_id):

    book = db.session.query(Book).filter(Book.id == book_id).first()

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            user_id = session.get('user_id')
            history = db.session.query(History).filter(History.user_id == user_id, History.book_id == book_id).first()

            # Update return date in a rental_history record
            history.return_date = datetime.datetime.today().strftime('%Y/%m/%d')
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('book/return.html', book=book)