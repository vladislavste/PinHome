from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Personal_area
from ext import db


class Personal_area_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Personal_area
        sqla_session = db.session
    id = fields.Integer(dump_only=True)
    surname = fields.String(required=True)
    name = fields.String(required=True)
    patronymic = fields.String(required=False)
    phone_number = fields.Boolean(required=False)
    email = fields.Integer(required=False)
    geolocation = fields.Date(required=False)
    id_user = fields.Integer(dump_only=True)
