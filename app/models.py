from app import db
from sqlalchemy import BigInteger


class User(db.Model):

    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    def __init__(self, username, email, password):

        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.id


class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.BigInteger)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128))
    publisher_name = db.Column(db.String(128))
    sales_date = db.Column(db.String(128))
    image_url = db.Column(db.String(128))
    donor = db.Column(db.String(128))


    def __init__(self, isbn, title, author, publisher_name, sales_date, image_url, donor):

        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher_name = publisher_name
        self.sales_date = sales_date
        self.image_url = image_url
        self.donor = donor

    def __repr__(self):
        return '<Book %r>' % self.id


class History(db.Model):

    __tablename__ = 'rental_history'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    checkout_date = db.Column(db.String(128), nullable=False)
    due_date = db.Column(db.String(128))
    return_date = db.Column(db.String(128))
    

    def __init__(self, book_id, user_id, checkout_date, due_date, return_date):

        self.book_id = book_id
        self.user_id = user_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = return_date

    def __repr__(self):
        return '<Lent %r>' % self.id