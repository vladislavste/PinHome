from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Chat_room(db.Model):
    __tablename__ = 'chat_room'
    id = db.Column(db.Integer, primary_key=True)
    chat_users = relationship("Chat_users", backref="chat_users")
    chat_message = relationship("Chat_message", backref="chat_message")

    def __init__(self):
        pass


class Chat_users(db.Model):
    __tablename__ = 'chat_users'
    id = db.Column(db.Integer, primary_key=True)
    chat_name = db.Column(db.String(200), nullable=True)
    id_sender = db.Column(db.Integer, nullable=False)
    id_addressee = db.Column(db.Integer, nullable=False)
    id_chat_room = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)

    def __init__(self, chat_name=None, id_sender=None, id_addressee=None, id_chat_room=None):
        self.chat_name = chat_name
        self.id_sender = id_sender
        self.id_addressee = id_addressee
        self.id_chat_room = id_chat_room


class Chat_message(db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(5000), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now())
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_chat_room = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)

    def __init__(self, message=None, created=None, id_user=None, id_chat_room=None):
        self.message = message
        self.id_user = id_user
        self.id_chat_room = id_chat_room


