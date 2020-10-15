from sqlalchemy import DateTime
from sqlalchemy.sql import func

from ext import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent = db.Column(db.Integer, nullable=True)


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    saled = db.Column(db.Boolean, default=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    deleted = db.Column(db.Boolean, default=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ImagesAnnoun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, nullable=True)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)


class Want(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    second = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    status = db.Column(db.Boolean, default=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
