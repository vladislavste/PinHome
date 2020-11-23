from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class AboutService(db.Model):
    __tablename__ = 'about_service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='О сервисе', nullable=True)
    image_path = db.Column(db.String, default='/images/about_service.png', nullable=True)
    description = db.Column(db.String(5000), nullable=False)

    def __init__(self, description):
        self.description = description