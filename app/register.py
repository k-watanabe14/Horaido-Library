from flask import Blueprint, request, render_template, flash, redirect, url_for, g, session
from werkzeug.exceptions import abort
from app.auth import login_required
from app.models import Book
from app import db
import requests
from app.forms import BookForm
from app.common import display_errors, get_new_image_url

# Define the blueprint: 'register', set its url prefix: app.url/register
mod_register = Blueprint('register', __name__, url_prefix='/register')

# ENHANCE: Add a function for searching books to register
@mod_register.route('/')
@login_required
def index():
    return render_template('register/index.html')


@mod_register.route('/isbn', methods=('GET', 'POST'))
def isbn():
    isbn = request.args.get('isbn')
    book = None

    form = BookForm()

    if isbn is not None:
        url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?applicationId=1053085901834686387&isbn=' + isbn
        response = requests.get(url)
        session.pop('_flashes', None)

        if 'Items' in response.json() and response.json()['Items']:
                book = response.json()['Items'][0]['Item']

        else:
            flash("該当する書籍が見つかりませんでした。再度ISBNを入力してください。")


    if request.method == 'POST' and book is None:
        isbn = request.form['isbn']
        return redirect(url_for('register.isbn', isbn=isbn))

    if book is not None:
        if form.validate_on_submit():
            if 'file' in request.files:
                try:
                    image_url = get_new_image_url(request.files['file'])
                except Exception as e:
                    flash("エラーが発生しました。もう一度やり直してください。")
                    return redirect(url_for('index'))
            else:
                image_url = book['largeImageUrl']
            isbn = request.form['isbn']
            title = request.form['title']
            author = request.form['author']
            publisher_name = request.form['publisher_name']
            sales_date = request.form['sales_date']
            borrower_id = None
            checkout_date = None

            data = Book(isbn, title, author, publisher_name, sales_date, image_url, borrower_id, checkout_date)
            db.session.add(data)
            db.session.commit()

            flash("本を登録しました。")
            return redirect(url_for('index'))

        else:
            display_errors(form.errors.items)

    return render_template('register/isbn.html', isbn=isbn, book=book, form=form)


@mod_register.route('/manual', methods=('GET', 'POST'))
def manual():

    form = BookForm()

    if form.validate_on_submit():
        image_url = None
        if 'file' in request.files:
            try:
                image_url = get_new_image_url(request.files['file'])
            except:
                flash("エラーが発生しました。もう一度やり直してください。")
                return redirect(url_for('index'))


        # Register book information into DB
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        publisher_name = request.form['publisher_name']
        sales_date = request.form['sales_date']
        borrower_id = None
        checkout_date = None

        data = Book(isbn, title, author, publisher_name, sales_date, image_url, borrower_id, checkout_date)
        db.session.add(data)
        db.session.commit()

        flash("本を登録しました。")
        return redirect(url_for('index'))

    else:
        display_errors(form.errors.items)

    return render_template('register/manual.html', form=form)
