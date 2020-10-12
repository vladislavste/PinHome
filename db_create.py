from app import app
from ext import db
def create_db(app):
    db.init_app(app)
    db.create_all(app)
