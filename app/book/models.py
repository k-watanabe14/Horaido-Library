from app import db


class HISTORY(db.Model):

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
