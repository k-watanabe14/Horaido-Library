from app import db


class User(db.Model):

    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = password
