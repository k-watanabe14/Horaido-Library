from app import db
from sqlalchemy import BigInteger


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
