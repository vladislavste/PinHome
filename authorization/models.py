from datetime import datetime
from ext import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    date_registration = db.Column(db.DateTime, default=datetime.utcnow(), nullable=True)
    have_personal_area = db.Column(db.Boolean, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=1, nullable=False)
    token = db.Column(db.String(500), nullable=False)

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        self.password = password
        self.token = token

    def __repr__(self):
        return f'<User {self.id}>'


class User_social(db.Model):
    __tablename__ = 'users_social'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(200), nullable=False, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
