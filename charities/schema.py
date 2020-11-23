from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Charities, Charity, Images_charities, Charities_address, Charities_contacts, Charities_social_networks
from ext import db


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


class Charities_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Charities
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=False)
    name = fields.String(required=True)
    description = fields.String(required=True)
    id_charity = fields.Integer(required=True)
    charities_address = fields.Nested(Charities_address_schema, many=True)
    charities_contacts = fields.Nested(Charities_contacts_schema, many=True)
    charities_social_networks = fields.Nested(Charities_social_networks_schema, many=True)
    images_charities = fields.Nested(Images_charities_schema, many=True)


class Charity_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Charity
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=False)
    name = fields.String(required=True)
    image_path = fields.String(required=True)
    charities = fields.Nested(Charities_schema, many=True)