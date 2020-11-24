from ext import db
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from authorization.authorization import token_check
from authorization.models import User
from helpers import allowed_file
from support.models import Support
from .schema import SupportSchema
import json
from uuid import uuid4
import os

support = Blueprint('support', __name__)


@support.route('/', methods=['GET'])
@token_check
def support_inforamtion(token):
    query = Support.query.first()
    support_schema = SupportSchema()
    all = support_schema.dump(query)
    return {"support": all}, 200


@support.route('/', methods=['POST'])
@token_check
def create_support_inforamtion(token):
    data = request.get_json()
    create = Support(description=data['description'])
    db.session.add(create)
    db.session.commit()
    return {'message': 'good!'}, 201