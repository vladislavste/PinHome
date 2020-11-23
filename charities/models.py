from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Charity(db.Model):
    __tablename__ = 'charity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='Социальные и экологические проекты', nullable=True)
    image_path = db.Column(db.String, default='/images/charity.png', nullable=True)
    charities = relationship("Charities", backref="charities")


class Charities(db.Model):
    __tablename__ = 'charities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=1, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    id_charity = db.Column(db.Integer, db.ForeignKey('charity.id'), nullable=False, unique=False)
    charities_address = relationship("Charities_address", backref="charities_address")
    charities_contacts = relationship("Charities_contacts", backref="charities_contacts")
    charities_social_networks = relationship("Charities_social_networks", backref="charities_social_networks")
    images_charities = relationship("Images_charities", backref="images_charities")


class Charities_address(db.Model):
    __tablename__ = 'charities_address'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), nullable=False)
    id_charities = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False, unique=False)


class Charities_contacts(db.Model):
    __tablename__ = 'charities_contacts'
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(500), nullable=False)
    id_charities = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False, unique=False)


class Charities_social_networks(db.Model):
    __tablename__ = 'charities_social_networks'
    id = db.Column(db.Integer, primary_key=True)
    social_networks = db.Column(db.String(500), nullable=False)
    id_charities = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False, unique=False)


class Images_charities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, nullable=True)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    id_charities = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False, unique=True)

