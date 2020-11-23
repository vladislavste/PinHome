from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Reference(db.Model):
    __tablename__ = 'reference'
    id = db.Column(db.Integer, primary_key=True)
    id_charity = db.Column(db.Integer, db.ForeignKey('charity.id'), nullable=False, unique=True)
    id_support = db.Column(db.Integer, db.ForeignKey('support.id'), nullable=False, unique=True)
    id_about_service = db.Column(db.Integer, db.ForeignKey('about_service.id'), nullable=False, unique=True)
    charity = relationship("Charity", backref="charity")
    support = relationship("Support", backref="support")
    about_service = relationship("AboutService", backref="about_service")

    def __init__(self, id_charity, id_support, id_about_service):
        self.id_charity = id_charity
        self.id_support = id_support
        self.id_about_service = id_about_service

