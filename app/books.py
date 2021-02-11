from flask import request, render_template, flash, session, redirect, \
    url_for, g, Blueprint
from app.auth import login_required
from app.models import Book, History, User, TagMaps, Tags
from app import app, db
import datetime
from dateutil.relativedelta import relativedelta
from app.forms import BookForm
from app.common import display_errors, get_new_image_url

# Define the blueprint: 'register', set its url prefix: app.url/register
mod_books = Blueprint('books', __name__, url_prefix='/books')


def borrow_book(user_id, book, book_id):
    checkout_date = datetime.datetime.today()
    due_date = (datetime.datetime.today() + relativedelta(months=1))
    return_date = None

    # Add history data into Rental History
    history_data = History(
        book_id, user_id, checkout_date, due_date, return_date)
    db.session.add(history_data)

    # Update book data in a book record
    borrower = User.query.get(user_id)
    book.borrower_id = borrower.id
    book.checkout_date = checkout_date

    db.session.commit()

    flash('「' + book.title + '」を貸しました。')


def return_book(book, book_id):
    history = History.query.filter(
        History.book_id == book_id, History.return_date == None).first()

    # Update return date in a rental_history record
    history.return_date = datetime.datetime.today()

    # Update Book data in a book record
    book.borrower_id = None
    book.checkout_date = None

    db.session.commit()

    flash('「' + book.title + '」を返しました。')


@mod_books.route('/<int:book_id>', methods=('GET', 'POST'))
def index(book_id):

    users = User.query
    book = Book.query.get(book_id)
    tags = TagMaps.query.filter_by(book_id=book.id).join(
        Tags).add_columns(Tags.tag_name)
    histories = History.query.filter_by(
        book_id=book.id).join(User).add_columns(User.username)

    if request.method == 'POST':
        if 'borrow_button' in request.form:
            user_id = request.form['borrower']
            borrow_book(user_id, book, book_id)
            app.logger.info('%s borrowed %s', g.user.username, book.title)
        elif 'return_button' in request.form:
            return_book(book, book_id)
            app.logger.info('%s returned %s', g.user.username, book.title)
        return redirect(url_for('books.index', book_id=book_id))

    # Page for Detail of book
    return render_template('books/index.html', users=users, book=book,
                           tags=tags, histories=histories)


# TODO: Add function to edit book tags
@mod_books.route('/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(book_id):

    book = Book.query.get(book_id)

    form = BookForm()

    tags = TagMaps.query.filter_by(book_id=book.id).join(
        Tags).add_columns(Tags.tag_name)

    if request.method == 'POST':
        if form.validate_on_submit():
            # Update image url
            if 'file' in request.files and \
                    request.files['file'].filename != '':
                try:
                    book.image_url = get_new_image_url(request.files['file'])
                except Exception as e:
                    flash('エラーが発生しました。もう一度やり直してください。')
                    app.logger.exception(
                        '%s failed to upload an image: %s', g.user.username, e)
                    return redirect(url_for('index'))

            # Update other data in a book record
            book.isbn = form.isbn.data
            book.title = form.title.data
            book.author = form.author.data
            book.publisher_name = form.publisher_name.data
            book.sales_date = form.sales_date.data

            db.session.commit()

            flash('保存しました。')
            app.logger.info('%s edited %s', g.user.username, book.title)
            return redirect(url_for('books.index', book_id=book_id))

        else:
            display_errors(form.errors.items)
            app.logger.info('%s failed to edit %s',
                            g.user.username, book.title)

    return render_template('books/edit.html', book=book, form=form, tags=tags)
