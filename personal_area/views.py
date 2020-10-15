from flask import Blueprint, request
from ext import db
from authorization.authorization import token_check
from authorization.models import User
from personal_area.models import Personal_area
from .schema import Personal_area_schema
import json

personal_area = Blueprint('personal_area', __name__)


@personal_area.route('/personal_area', methods=['POST'])
@token_check
def create_personal_area(token):
    data = request.get_json()
    #data2 = json.loads(request.form['request'])
    if 'surname' in data and 'name' in data:
        if data['surname'] == '' or data['name'] == '':
            return {'error': 'Empty fields'}, 400
        get_user = User.query.filter(User.token == token).one()
        check_personal_area = db.session.query(Personal_area).filter_by(id_user=get_user.id).first()
        if not check_personal_area:
            try:
                personal_area = Personal_area(
                    surname=data['surname'],
                    name=data['name'],
                    id_user=get_user.id
                )
                if 'patronymic' in data:
                    personal_area.patronymic = data['patronymic']
                if 'phone_number' in data:
                    personal_area.phone_number = data['phone_number']
                if 'email' in data:
                    personal_area.email = data['email']
                if 'geolocation' in data:
                    personal_area.geolocation = data['geolocation']
                # data['id_user'] = get_user.id
                # personal_area_schema = Personal_area_schema()
                # personal_area = personal_area_schema.load(data)
                db.session.add(personal_area)
                db.session.commit()
                return {'message': 'successfully!'}, 201
            except:
                return {'message': 'error create'}, 401
        return {'error': 'Personal_area is already registered'}, 200
    return {'error': 'Empty fields'}, 400


@personal_area.route('/personal_area/<id>', methods=['GET'])
@token_check
def read_personal_area(token, id):
    currently_user = Personal_area.query.filter(Personal_area.id_user == id).one()
    personal_area_schema = Personal_area_schema()
    currently_user = personal_area_schema.dump(currently_user)
    return {'personal_area_by_id': currently_user}


@personal_area.route('/personal_area', methods=['PUT'])
@token_check
def update_personal_area(token):
    get_user = User.query.filter(User.token == token).one()
    check_personal_area = db.session.query(Personal_area).filter_by(id_user=get_user.id).first()
    if check_personal_area:
        data = request.get_json()
        try:
            if 'surname' in data:
                if data['surname'] != '':
                    personal_area.surname = data['surname']
            if 'name' in data:
                if data['name'] != '':
                    personal_area.name = data['name']
            if 'patronymic' in data:
                personal_area.patronymic = data['patronymic']
            if 'phone_number' in data:
                personal_area.phone_number = data['phone_number']
            if 'email' in data:
                personal_area.email = data['email']
            if 'geolocation' in data:
                personal_area.geolocation = data['geolocation']
            db.session.add(personal_area)
            db.session.commit()
            return {'message': 'successfully!'}, 201
        except:
            return {'message': 'error edit personal area'}, 401
    return {'error': 'Personal_area not found'}, 401


@personal_area.route('/personal_area', methods=['DELETE'])
@token_check
def delete_personal_area(token):
    get_user = User.query.filter(User.token == token).one()
    check_personal_area = db.session.query(Personal_area).filter_by(id_user=get_user.id).first()
    personal_area = Personal_area.query.get(check_personal_area.id)
    if personal_area:
        personal_area.deleted = True
        db.session.add(personal_area)
        db.session.commit()
        return {"message": 'User is deleted'}, 200
    return {'error': 'Personal_area not found'}, 401
