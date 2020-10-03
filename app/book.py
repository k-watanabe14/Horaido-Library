from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth import login_required
from app.models import Book, History, User
from app import db
from app.auth import load_logged_in_user
import datetime
from dateutil.relativedelta import relativedelta
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_book = Blueprint('book', __name__, url_prefix='/book')


@mod_book.route('/<int:book_id>')
@login_required
def index(book_id):

    book = Book.query.filter_by(id=book_id).first()
    histories = History.query.filter_by(book_id=book.id)

    # Page for Detail of book
    return render_template('book/index.html', book=book, histories=histories)


@mod_book.route('/<int:book_id>/borrow', methods=('GET', 'POST'))
@login_required
def borrow(book_id):

    book = Book.query.filter_by(id=book_id).first()

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            user_id = session.get('user_id')
            user_name = session.get('user_name')
            checkout_date = datetime.datetime.today().strftime('%Y/%m/%d')
            due_date = (datetime.datetime.today() + relativedelta(months=1)).strftime('%Y/%m/%d')
            return_date = None

            # Add history data into Rental History
            history_data = History(book_id, user_id, user_name, checkout_date, due_date, return_date)
            db.session.add(history_data)

            # Update book data in a book record
            borrower = User.query.filter_by(id=user_id).first()
            book.borrower_id = borrower.id
            book.borrower_name = borrower.username
            book.checkout_date = checkout_date
            
            db.session.commit()

            flash(book.title + "を借りました。")

            return redirect(url_for('index'))

    return render_template('book/borrow.html', book=book)


@mod_book.route('/<int:book_id>/return', methods=('GET', 'POST'))
@login_required
def return_(book_id):

    book = Book.query.filter_by(id=book_id).first()

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            user_id = session.get('user_id')
            history = History.query.filter(History.user_id==user_id, History.book_id==book_id).first()

            # Update return date in a rental_history record
            history.return_date = datetime.datetime.today().strftime('%Y/%m/%d')
            
            # Update Book data in a book record
            book.borrower_id = None
            book.borrower_name = None
            book.checkout_date = None
            
            db.session.commit()

            flash(book.title + "を返しました。")

            return redirect(url_for('index'))

    return render_template('book/return.html', book=book)


@mod_book.route('/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(book_id):

    book = Book.query.filter_by(id=book_id).first()   

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            # Update date in a book record
            title = request.form['title']
            author = request.form['author']
            publisher_name = request.form['publisher_name']
            sales_date = request.form['sales_date']
            donor = request.form['donor']            
            db.session.commit()
            flash('編集しました')
            return redirect(url_for('index'))

    return render_template('book/edit.html', book=book)