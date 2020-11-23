from ext import db
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from authorization.authorization import token_check
from authorization.models import User
from helpers import allowed_file
from .models import Reference
from .schema import ReferenceSchema
import json
from uuid import uuid4
import os

reference = Blueprint('reference', __name__)


@reference.route('/', methods=['GET'])
@token_check
def all_reference(token):
    query = Reference.query.first()
    reference_schema = ReferenceSchema()
    all = reference_schema.dump(query)
    return {"reference": all}, 200


@reference.route('/', methods=['POST'])
@token_check
def create_reference(token):
    data = request.get_json()
    create = Reference(id_charity=data['id_charity'], id_support=data['id_support'],
                       id_about_service=data['id_about_service'])
    db.session.add(create)
    db.session.commit()
    return {'message': 'good!'}, 201