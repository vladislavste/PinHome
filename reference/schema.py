from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Reference
from about_service.schema import AboutServiceSchema
from charities.schema import Charity_schema
from support.schema import SupportSchema
from ext import db


class ReferenceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Reference
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=False)
    support = fields.Nested(SupportSchema)
    about_service = fields.Nested(AboutServiceSchema)
    charity = fields.Nested(Charity_schema)