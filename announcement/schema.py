from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Announcement, ImagesAnnoun
from ext import db


class AnnouncementSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Announcement
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    saled = fields.Boolean(required=False)
    category = fields.Integer(required=True)
    created_date = fields.Date(dump_only=True)
    user = fields.Integer(required=True)


class AnnouncementImageSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ImagesAnnoun
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    image_path = fields.String(required=True)
    created = fields.Date(dump_only=True)
    announcement = fields.Number(required=True)
