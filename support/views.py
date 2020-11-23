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
    query = Support.query.all()
    support_schema = SupportSchema()
    all = support_schema.dump(query)
    return {"support": all}, 200