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
    query = Reference.query.all()
    reference_schema = ReferenceSchema()
    all = reference_schema.dump(query, many=True)
    return {"reference": all}, 200
