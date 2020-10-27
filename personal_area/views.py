import json
import os
from uuid import uuid4

from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from authorization.authorization import token_check
from authorization.models import User
from ext import db
from helpers import allowed_file
from personal_area.models import Personal_area, Images_personal_area
from .schema import Personal_area_schema, Images_personal_area_schema

personal_area = Blueprint('personal_area', __name__)


@personal_area.route('/', methods=['POST'])
@token_check
def create_personal_area(token):
    data = json.loads(request.form['request'])
    if 'surname' in data and 'name' in data:
        if data['surname'] == '' or data['name'] == '':
            return {'error': 'Empty fields'}, 400
        try:
            get_user = User.query.filter(User.token == token).one()
        except:
            return {'error': 'Personal_area not found'}, 401
        check_personal_area = db.session.query(Personal_area).filter_by(id_user=get_user.id).first()
        if not check_personal_area:

                personal_area_schema = Personal_area_schema()
                data['id_user'] = get_user.id
                personal_area = personal_area_schema.load(data)
                db.session.add(personal_area)
                db.session.flush()
                id = personal_area.id

                user = User.query.get(get_user.id)
                user.have_personal_area = 1
                db.session.add(user)

                image_schema = Images_personal_area_schema()

                if request.files.get('photo'):
                    file = request.files.get('photo')
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        extension = filename.split()[-1]
                        new_filename = "upload-{}.{}".format(
                            uuid4(), extension
                        )

                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER_PERSONAL_AREA'], new_filename))
                        img_data = {
                            "image_path": f'/images/personal_area/{new_filename}',
                            "id_personal_area": id
                        }
                        db_image = image_schema.load(img_data)
                        db.session.add(db_image)
                else:
                    img_data = {
                        "image_path": f'/images/default.jpg',
                        "id_personal_area": id
                    }
                    db_image = image_schema.load(img_data)
                    db.session.add(db_image)

                db.session.commit()
                return {'message': 'successfully!'}, 201

        return {'error': 'Personal_area is already registered'}, 200
    return {'error': 'Empty fields'}, 400


@personal_area.route('/<id>', methods=['GET'])
@token_check
def read_personal_area(token, id):
    try:
        get_personal_area = Personal_area.query.filter(Personal_area.id == id).one()
        personal_area_schema = Personal_area_schema()
        currently_user = personal_area_schema.dump(get_personal_area)
        get_photo = db.session.query(Images_personal_area).filter_by(id_personal_area=get_personal_area.id).first()
        image_schema = Images_personal_area_schema()
        photo = image_schema.dump(get_photo)
        return {
            'currently_user': currently_user,
            'photo': photo,
        }, 200
    except:
        return {'error': 'User not found'}, 401


@personal_area.route('/', methods=['PUT'])
@token_check
def update_personal_area(token):
    try:
        get_user = User.query.filter(User.token == token).one()
    except:
        return {'error': 'Personal_area not found'}, 401
    personal_area = db.session.query(Personal_area).filter_by(id_user=get_user.id).first()
    if personal_area:
        if request.form:
            data = json.loads(request.form['request'])
            try:
                personal_area = Personal_area.query.get(personal_area.id)
                if data.get('surname'):
                    if data['surname'] != '':
                        personal_area.surname = data['surname']
                if data.get('name'):
                    if data['name'] != '':
                        personal_area.name = data['name']
                if data.get('patronymic'):
                    personal_area.patronymic = data['patronymic']
                if data.get('phone_number'):
                    personal_area.phone_number = data['phone_number']
                if data.get('email'):
                    personal_area.email = data['email']
                if data.get('geolocation'):
                    personal_area.geolocation = data['geolocation']

                db.session.add(personal_area)
            except:
                return {'message': 'error edit personal area'}, 401
        try:
            image_schema = Images_personal_area_schema()
            file = request.files.get('photo')
            if file and allowed_file(file.filename):
                get_photo = db.session.query(Images_personal_area).filter_by(id_personal_area=personal_area.id).first()
                if get_photo:
                    photo = Images_personal_area.query.get(get_photo.id)
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

                file.save(os.path.join(current_app.config['UPLOAD_FOLDER_PERSONAL_AREA'], new_filename))
                img_data = {
                    "image_path": f'/images/personal_area/{new_filename}',
                    "id_personal_area": personal_area.id
                }
                db_image = image_schema.load(img_data)
                db.session.add(db_image)
        except:
            return {'message': 'error edit photo'}, 401
        db.session.commit()
        return {'message': 'successfully!'}, 201
    return {'error': 'Personal_area not found'}, 401


@personal_area.route('/', methods=['DELETE'])
@token_check
def delete_personal_area(token):
    get_user = User.query.filter(User.token == token).one()
    user = User.query.get(get_user.id)
    user.is_active = 0
    db.session.add(user)
    db.session.commit()
    return {"message": 'User is deleted'}, 200


@personal_area.route('/change_password', methods=['POST'])
@token_check
def change_password(token):
    data = request.get_json()
    if data['old_password'] != '' and data['new_password'] != '':
        get_user = User.query.filter(User.token == token).one()
        check_password = check_password_hash(get_user.password, data['old_password'])
        if check_password:
            user = User.query.get(get_user.id)
            hash_password = generate_password_hash(data['new_password'], method='sha256')
            user.password = hash_password
            db.session.add(user)
            db.session.commit()
            return {'message': 'Password changed'}, 200
        return {'error': 'Old password incorrect'}, 400
    return {'error': 'Empty fields'}, 400
