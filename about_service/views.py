from ext import db
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from authorization.authorization import token_check
from authorization.models import User
from helpers import allowed_file
from about_service.models import AboutService
from .schema import AboutServiceSchema
import json
from uuid import uuid4
import os

about_service = Blueprint('about_service', __name__)


@about_service.route('/', methods=['GET'])
@token_check
def about_service_inforamtion(token):
    query = AboutService.query.all()
    about_service_schema = AboutServiceSchema()
    all = about_service_schema.dump(query)
    return {"about_service": all}, 200