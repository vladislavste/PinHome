from datetime import datetime
from ext import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    date_registration = db.Column(db.DateTime, default=datetime.utcnow(), nullable=True)
    token = db.Column(db.String(500), nullable=False)

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        self.password = password
        self.token = token

    def __repr__(self):
        return f'<User {self.id}>'
