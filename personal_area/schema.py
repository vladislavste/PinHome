from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from ext import db
from .models import Personal_area, Images_personal_area


class Personal_area_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Personal_area
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    surname = fields.String(required=True)
    name = fields.String(required=True)
    patronymic = fields.String(required=False)
    phone_number = fields.String(required=False)
    email = fields.String(required=False)
    geolocation = fields.String(required=False)
    id_user = fields.Integer(required=True)


class Images_personal_area_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Images_personal_area
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    image_path = fields.String(required=True)
    created = fields.Date(dump_only=True)
    id_personal_area = fields.Integer(required=True)
