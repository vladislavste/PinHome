from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Support(db.Model):
    __tablename__ = 'support'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, nullable=True)
    description = db.Column(db.String(5000), nullable=False)