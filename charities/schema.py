from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Charities, Images_charities, Charities_address, Charities_contacts, Charities_social_networks
from ext import db


class Charities_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Charities
        sqla_session = db.session

    id = fields.Integer(dump_only=False)
    name = fields.String(required=True)
    description = fields.String(required=True)


class Charities_social_networks_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Charities_social_networks
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    social_networks = fields.String(required=True, many=True)
    id_charities = fields.Integer(required=True)


class Charities_contacts_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Charities_contacts
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    contact = fields.String(required=True, many=True)
    id_charities = fields.Integer(required=True)


class Charities_address_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Charities_address
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    address = fields.String(required=True, many=True)
    id_charities = fields.Integer(required=True)


class Images_charities_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Images_charities
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    image_path = fields.String(required=True)
    created = fields.Date(dump_only=True)
    id_charities = fields.Integer(required=True)
