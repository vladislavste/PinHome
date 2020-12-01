from marshmallow_sqlalchemy import ModelSchema, auto_field
from marshmallow import fields, pre_dump
from .models import Announcement, ImagesAnnoun, Category, Want, RecentlyViewed, TypeClose, ReasonClose, Closed
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


class AllCategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        sqla_session = db.session
        include_relationships = False
        load_instance = False
        include_fk = True

    id = fields.Integer(required=False)
    name = fields.String(required=False)
    parent = fields.Integer(required=False)


class WantSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Want
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(required=False)
    announcement = fields.Integer(load_only=True, required=False)
    str_want = fields.String(required=True)
    category = fields.Integer(load_only=True, required=True)
    want_cat = fields.Nested(CategorySchema, dump_only=True, only=["id", "name"])


class CategoryWithAnnouncmentsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        sqla_session = db.session

    id = fields.Integer(required=False)
    name = fields.String(required=False)
    parent = fields.Integer(required=False)


class TypeCloseSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = TypeClose
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class ReasonCloseSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ReasonClose
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class ClosedSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Closed
        sqla_session = db.session
        include_relationships = False

    id = fields.Integer(dump_only=True)
    type = fields.Integer(required=True, )
    reason = fields.Integer(required=True)


class ClosedNestedSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Closed
        sqla_session = db.session

    id = fields.Integer()
    reason_close = fields.Nested(TypeCloseSchema, dump_only=True)
    type_close = fields.Nested(ReasonCloseSchema, dump_only=True)


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
    reason = fields.Nested(ClosedNestedSchema, dump_only=True)
    no_exchange = fields.Boolean(required=False)

class RecentlyViewedSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RecentlyViewed
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    recently_viewed = fields.Nested(AnnouncementSchema, only=["id", "name", "user", "images", "want"])
    created = fields.DateTime(dump_only=True)
