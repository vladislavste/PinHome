import json
from flask import Blueprint, request
from authorization.authorization import token_check
from authorization.models import User
from ext import db
from chat.models import Chat_users, Chat_room, Chat_message
from chat.schema import Chat_message_schema, Chat_room_schema, Chat_users_schema
from personal_area.models import Personal_area

chat = Blueprint('chat', __name__)


@chat.route('/', methods=['GET'])
@token_check
def get_all_chats(token):
    get_user = User.query.filter(User.token == token).one()
    all_chats = Chat_users.query.filter(Chat_users.id_sender == get_user.id).all()
    chat_users_schema = Chat_users_schema()
    all_chats = chat_users_schema.dump(all_chats, many=True)
    return {'chats': all_chats}, 200


@chat.route('/<id>', methods=['GET'])
@token_check
def get_chat_by_id_user(token, id):
    get_user = User.query.filter(User.token == token).one()
    check_chat = db.session.query(Chat_users).filter_by(id_sender=get_user.id, id_addressee=id).first()
    if check_chat:
        chat = Chat_room.query.get(check_chat.id_chat_room)
        chat_room_schema = Chat_room_schema()
        chat_room_dump = chat_room_schema.dump(chat)
        return chat_room_dump, 200
    else:
        try:
            chat_room = Chat_room()
            db.session.add(chat_room)
            db.session.flush()
            id_chat_room = chat_room.id
            personal_area_sender = Personal_area.query.filter(Personal_area.id_user == get_user.id).one()
            personal_area_addressee = Personal_area.query.filter(Personal_area.id_user == id).one()
            chat_users = Chat_users(chat_name=personal_area_addressee.surname, id_sender=get_user.id, id_addressee=id,
                                    id_chat_room=id_chat_room)
            db.session.add(chat_users)
            chat_users = Chat_users(chat_name=personal_area_sender.surname, id_sender=id, id_addressee=get_user.id,
                                    id_chat_room=id_chat_room)
            db.session.add(chat_users)
            db.session.commit()

            chat = Chat_room.query.get(id_chat_room)
            chat_room_schema = Chat_room_schema()
            chat_room_dump = chat_room_schema.dump(chat)
            return chat_room_dump, 200
        except:
            return {'error': 'Personal area not found'}, 401


@chat.route('/<id>', methods=['POST'])
@token_check
def send_message(token, id):
    get_user = User.query.filter(User.token == token).one()
    get_chat = db.session.query(Chat_users).filter_by(id_sender=get_user.id, id_addressee=id).first()
    if get_chat:
        data = request.get_json()
        if data['message'] != '':
            chat_message = Chat_message(message=data['message'], id_user=get_user.id,
                                        id_chat_room=get_chat.id_chat_room)
            db.session.add(chat_message)
            db.session.commit()
            return {'error': 'Message is sended'}, 200
    return {'error': 'Personal area not found'}, 401