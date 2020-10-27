from marshmallow_sqlalchemy import ModelSchema, auto_field
from marshmallow import fields, pre_dump
from .models import Announcement, ImagesAnnoun, Category, Want, RecentlyViewed
from ext import db




class AnnouncementImageSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ImagesAnnoun
        sqla_session = db.session


    id = fields.Integer(dump_only=True)
    image_path = fields.String(required=True)
    created = fields.Date(dump_only=True)
    announcement = fields.Integer(required=True)

class CategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        sqla_session = db.session

    id = fields.Integer(required=False)
    name = fields.String(required=False)
    parent = fields.Integer(required=False)


class WantSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Want
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    announcement = fields.Integer(required=False)
    category =fields.Integer(required=True)


class AnnouncementSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Announcement
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(required=False)
    name = fields.String(required=True)
    description = fields.String(required=True)
    saled = fields.Boolean(required=False)
    category = fields.Integer(required=True)
    created_date = fields.Date(dump_only=True)
    user = fields.Integer(required=True)
    images = fields.Nested(AnnouncementImageSchema, many=True)
    want = fields.Nested(WantSchema, many=True)
    city = fields.String(required=False)
    address = fields.String(required=False)


class CategoryWithAnnouncmentsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        sqla_session = db.session

    id = fields.Integer(required=False)
    name = fields.String(required=False)
    parent = fields.Integer(required=False)


class RecentlyViewedSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RecentlyViewed
        sqla_session = db.session
        include_relationships = True
        load_instance = True


    id = fields.Integer(dump_only=True)
    recently_viewed = fields.Nested(AnnouncementSchema, only=["id", "name", "user", "images", "want"])
    created = fields.DateTime(dump_only=True)
