from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ext import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent = db.Column(db.Integer, nullable=True)
    products = relationship("Announcement", backref="announcement")


class ImagesAnnoun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, nullable=True)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    saled = db.Column(db.Boolean, default=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    deleted = db.Column(db.Boolean, default=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    images = relationship("ImagesAnnoun", backref="images_announ")
    want = relationship("Want", backref="want")
    recently_viewed = relationship("RecentlyViewed", backref="recently_viewed")


class Want(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    second = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    status = db.Column(db.Boolean, default=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())


class RecentlyViewed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
