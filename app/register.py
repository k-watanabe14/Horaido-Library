from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth import login_required
from app.models import Book
from app import db
import requests
import io
import datetime
from app.s3 import upload_file
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_register = Blueprint('register', __name__, url_prefix='/register')


@mod_register.route('/')
def index():
    return render_template('register/index.html')


@mod_register.route('/isbn', methods=('GET', 'POST'))
def isbn():
    isbn = request.args.get('isbn')
    book_data = None

    if isbn is not None:
        url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?applicationId=1053085901834686387&isbn=' + isbn
        response = requests.get(url)
        book_data = response.json()['Items'][0]['Item']

    if request.method == 'POST' and book_data is None:
        isbn = request.form['isbn']
        return redirect(url_for('register.isbn', isbn=isbn))

    if request.method == 'POST' and book_data is not None:
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        publisher_name = request.form['publisher_name']
        sales_date = request.form['sales_date']
        image_url = book_data['largeImageUrl']
        borrower_id = None
        checkout_date = None

        data = Book(isbn, title, author, publisher_name, sales_date, image_url, borrower_id, checkout_date)
        db.session.add(data)
        db.session.commit()

        flash("本を登録しました。")
        return redirect(url_for('index'))

    return render_template('register/isbn.html', isbn=isbn, book_data=book_data)


@mod_register.route('/manual', methods=('GET', 'POST'))
def manual():

    if request.method == 'POST':
        # Save book image into S3 and set image url
        if 'book_image' in request.files:
            image = request.files['book_image']
            image_name = datetime.datetime.now().isoformat() + ".jpg"
            body = io.BufferedReader(image).read()
            key = f'books/{image_name}'
            upload_file(body, key, 'image/jpeg')
            image_url = "https://houraidou-images.s3.us-east-2.amazonaws.com/books/" + image_name
        else:
            image_url = None

        # Register book infromation into DB
        isbn = request.form['isbn'] if request.form['isbn'] != '' else None
        c_code = request.form['c-code'] if request.form['c-code'] != '' else None
        title = request.form['title']
        author = request.form['author']
        publisher_name = request.form['publisher_name']
        sales_date = request.form['sales_date']
        donor = request.form['donor']
        borrower_id = None
        borrower_name = None
        checkout_date = None

        data = Book(isbn, c_code, title, author, publisher_name, sales_date, image_url, donor, borrower_id, borrower_name, checkout_date)
        db.session.add(data)
        db.session.commit()

        flash("本を登録しました。")
        return redirect(url_for('index'))

    return render_template('register/manual.html')
    