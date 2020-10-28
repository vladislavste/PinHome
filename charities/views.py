from ext import db
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from authorization.authorization import token_check
from authorization.models import User
from helpers import allowed_file
from charities.models import Charities, Charities_address, Charities_contacts, Charities_social_networks, Images_charities
from .schema import Charities_address_schema, Charities_contacts_schema, Charities_social_networks_schema, Images_charities_schema, Charities_schema
import json
from uuid import uuid4
import os

charities = Blueprint('charities', __name__)


@charities.route('/', methods=['GET'])
@token_check
def all_charities(token):
    query = Charities.query.all()
    charities_schema = Charities_schema()
    all = charities_schema.dump(query, many=True)
    return {"charities": all}, 200


@charities.route('/<id>', methods=['GET'])
@token_check
def one_charities(token, id):
    try:
        charities = Charities.query.get(id)
    except:
        return {'error': 'Charities not found'}, 401
    charities_schema = Charities_schema()
    charities_dump = charities_schema.dump(charities)
    return charities_dump, 200


@charities.route('/', methods=['POST'])
@token_check
def create_charities(token):
    get_user = User.query.filter(User.token == token).one()
    if get_user.username == 'Admin' or get_user.username == 'admin':
        try:
            data_charities = json.loads(request.form['charities'])
            check_charities = db.session.query(Charities).filter_by(name=data_charities['name']).first()
            if check_charities:
                return {'error': 'Charities is already registered'}, 200
            сharities_schema = Charities_schema()
            charities = сharities_schema.load(data_charities)
            db.session.add(charities)
            db.session.flush()
            id = charities.id

            data_for_charities_address = json.loads(request.form['charities_address'])
            charities_address_schema = Charities_address_schema()
            for val in data_for_charities_address['address']:
                data_charities_address = {
                    'address': val,
                    'id_charities': id
                }
                charities_address = charities_address_schema.load(data_charities_address)
                db.session.add(charities_address)

            data_for_charities_contacts = json.loads(request.form['charities_contacts'])
            charities_contacts_schema = Charities_contacts_schema()
            for val in data_for_charities_contacts['contact']:
                data_charities_contacts = {
                    'contact': val,
                    'id_charities': id
                }
                charities_contacts = charities_contacts_schema.load(data_charities_contacts)
                db.session.add(charities_contacts)

            data_for_charities_social_networks = json.loads(request.form['charities_social_networks'])
            charities_social_networks_schema = Charities_social_networks_schema()
            for val in data_for_charities_social_networks['social_networks']:
                data_charities_social_networks = {
                    'social_networks': val,
                    'id_charities': id
                }
                charities_social_networks = charities_social_networks_schema.load(data_charities_social_networks)
                db.session.add(charities_social_networks)

            image_schema = Images_charities_schema()
            if request.files.get('photo'):
                file = request.files.get('photo')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = filename.split()[-1]
                    new_filename = "upload-{}.{}".format(
                        uuid4(), extension
                    )

                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER_CHARITIES'], new_filename))
                    img_data = {
                        "image_path": f'/images/charities/{new_filename}',
                        "id_charities": id
                    }
                    db_image = image_schema.load(img_data)
                    db.session.add(db_image)
            else:
                img_data = {
                    "image_path": f'/images/default.jpg',
                    "id_charities": id
                }
                db_image = image_schema.load(img_data)
                db.session.add(db_image)
            db.session.commit()
            return {'message': 'successfully!'}, 201
        except:
            return {'error': 'Error in data'}, 400
    return {'error': 'You not admin!'}, 401


@charities.route('/<id>', methods=['PUT'])
@token_check
def update_charities(token, id):
    get_user = User.query.filter(User.token == token).one()
    if get_user.username == 'Admin' or get_user.username == 'admin':
        try:
            charities = Charities.query.get(id)
        except:
            return {'error': 'Charities not found'}, 401
        if request.form:
            data = json.loads(request.form['charities'])
            data['id'] = id
            сharities_schema = Charities_schema()
            charities = сharities_schema.load(data=data)
            db.session.add(charities)
            db.session.commit()
            try:
                image_schema = Images_charities_schema()
                file = request.files.get('photo')
                if file and allowed_file(file.filename):
                    get_photo = db.session.query(Images_charities).filter_by(id_charities=id).first()
                    if get_photo:
                        photo = Images_charities.query.get(get_photo.id)
                        db.session.delete(photo)
                        if photo.image_path != '/images/default.jpg':
                            path_delete = current_app.config['PROJECT_HOME'] + photo.image_path
                            os.remove(path_delete)
                        db.session.commit()

                    filename = secure_filename(file.filename)
                    extension = filename.split()[-1]
                    new_filename = "upload-{}.{}".format(
                        uuid4(), extension
                    )

                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER_CHARITIES'], new_filename))
                    img_data = {
                        "image_path": f'/images/charities/{new_filename}',
                        "id_charities": id
                    }
                    db_image = image_schema.load(img_data)
                    db.session.add(db_image)
            except:
                return {'message': 'error edit photo'}, 401
            db.session.commit()
            return {'message': 'successfully!'}, 201
    return {'error': 'You not admin!'}, 401


@charities.route('/<id>', methods=['DELETE'])
@token_check
def delete_charities(token, id):
    get_user = User.query.filter(User.token == token).one()
    if get_user.username == 'Admin' or get_user.username == 'admin':
        сharities = Charities.query.get(id)
        сharities.is_active = 0
        db.session.add(сharities)
        db.session.commit()
        return {"message": 'Charities is deleted'}, 200
    return {'error': 'You not admin!'}, 401
