from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Support
from ext import db


class SupportSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Support
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    image_path = fields.String(required=True)
    description = fields.String(required=True)
