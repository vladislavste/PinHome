from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Chat_room, Chat_users, Chat_message
from ext import db


class Chat_message_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Chat_message
        sqla_session = db.session

    id = fields.Integer(dump_only=False)
    message = fields.String(required=True, many=True)
    created = fields.Date(dump_only=True)
    id_user = fields.Integer(required=True)
    id_chat_room = fields.Integer(required=True)


class Chat_users_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Chat_users
        sqla_session = db.session

    id = fields.Integer(dump_only=False)
    id_sender = fields.Integer(required=True)
    id_addressee = fields.Integer(required=True)
    id_chat_room = fields.Integer(required=True)


class Chat_room_schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Chat_room
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=False)
    chat_name = fields.String(required=True)
    chat_users = fields.Nested(Chat_users_schema, many=True)
    chat_message = fields.Nested(Chat_message_schema, many=True)