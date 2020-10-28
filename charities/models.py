from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Charities(db.Model):
    __tablename__ = 'charities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=1, nullable=False)
    description = db.Column(db.String(5000), nullable=False)


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

