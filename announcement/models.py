from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ext import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)
    products = relationship("Announcement", backref="announcement")
    want = relationship("Want", backref="want_cat")


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
    reason_id = db.Column(db.Integer, db.ForeignKey('closed.id'), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    images = relationship("ImagesAnnoun", backref="images_announ")
    want = relationship("Want", backref="want")
    recently_viewed = relationship("RecentlyViewed", backref="recently_viewed")
    reason = relationship("Closed", backref="closed")
    delete = db.Column(db.Boolean, default=False, unique=False)
    no_exchange = db.Column(db.Boolean, default=False, unique=False)
    str_want = db.Column(db.String(300), nullable=True)
    # full_user_data = relationship("User", backref="user_data")


class Want(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())


class Closed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey('type_close.id'), nullable=False)
    reason = db.Column(db.Integer, db.ForeignKey('reason_close.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    reason_close = relationship("ReasonClose", backref="reason_closed")
    type_close = relationship("TypeClose", backref="type_closed")


class TypeClose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


class ReasonClose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


class RecentlyViewed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
