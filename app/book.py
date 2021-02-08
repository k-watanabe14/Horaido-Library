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
mod_book = Blueprint('book', __name__, url_prefix='/book')


def borrow_book(book, book_id):
    user_id = session.get('user_id')
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

    flash('「' + book.title + '」を借りました。')


def return_book(book, book_id):
    user_id = session.get('user_id')
    history = History.query.filter(
        History.user_id == user_id, History.book_id == book_id).first()

    # Update return date in a rental_history record
    history.return_date = datetime.datetime.today()

    # Update Book data in a book record
    book.borrower_id = None
    book.checkout_date = None

    db.session.commit()

    flash('「' + book.title + '」を返しました。')


@mod_book.route('/<int:book_id>', methods=('GET', 'POST'))
@login_required
def index(book_id):

    book = Book.query.get(book_id)
    tags = TagMaps.query.filter_by(book_id=book.id).join(
        Tags).add_columns(Tags.tag_name)
    histories = History.query.filter_by(
        book_id=book.id).join(User).add_columns(User.username)

    if request.method == 'POST':
        if 'borrow_button' in request.form:
            borrow_book(book, book_id)
            app.logger.info('%s borrowed %s', g.user.username, book.title)
        elif 'return_button' in request.form:
            return_book(book, book_id)
            app.logger.info('%s returned %s', g.user.username, book.title)
        return redirect(url_for('book.index', book_id=book_id))

    # Page for Detail of book
    return render_template('book/index.html', book=book,
                           tags=tags, histories=histories)


# TODO: Add function to edit book tags
@mod_book.route('/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(book_id):

    book = Book.query.get(book_id)

    form = BookForm()

    tags = TagMaps.query.filter_by(book_id=book.id).join(
        Tags).add_columns(Tags.tag_name)

    if form.validate_on_submit():
        # Update image url
        if 'file' in request.files and request.files['file'].filename != '':
            try:
                book.image_url = get_new_image_url(request.files['file'])
            except Exception as e:
                flash('エラーが発生しました。もう一度やり直してください。')
                app.logger.exception(
                    '%s could not upload an image: %s', g.user.username, e)
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
        return redirect(url_for('book.index', book_id=book_id))

    else:
        display_errors(form.errors.items)

    return render_template('book/edit.html', book=book, form=form, tags=tags)
