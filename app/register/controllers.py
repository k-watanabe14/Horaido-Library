from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth.controllers import login_required
from app.register.models import Book
from app import db
import requests
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_register = Blueprint('register', __name__, url_prefix='/register')


@mod_register.route('/')
@login_required
def index():
    return render_template('register/index.html')


@mod_register.route('/auto', methods=('GET', 'POST'))
@login_required
def auto():
    isbn = request.args.get('isbn')
    book_data =[]

    if request.method == 'POST' and isbn is None:
        isbn = request.form['isbn']
        error = None

        if not isbn:
            error = 'isbn is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('register.auto', isbn = isbn))

    if isbn is not None:
        url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?applicationId=1053085901834686387&isbn=' + isbn
        response = requests.get(url)
        book_data = response.json()['Items'][0]['Item']

        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            publisher_name = request.form['publisher_name']
            sales_date = request.form['sales_date']
            image_url = book_data['largeImageUrl']
            donor = request.form['donor']

            data = Book(isbn, title, author, publisher_name, sales_date, image_url, donor)
            db.session.add(data)
            db.session.commit()

            return redirect(url_for('register.success'))

    return render_template('register/auto.html', isbn = isbn, book_data = book_data)


@mod_register.route('/success')
@login_required
def success():
    return render_template('register/success.html')
    