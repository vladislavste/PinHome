from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from authorization.models import User, User_social
from ext import db
import uuid
from authorization.authorization import token_check, OAuthSignIn

authorization = Blueprint('authorization', __name__)


@authorization.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    user = db.session.query(User).filter_by(username=data['username']).first()
    if user and user.is_active == 1:
        check_password = check_password_hash(user.password, data['password'])
        if check_password:
            get_user = User.query.filter(User.token == user.token).one()
            res = make_response({
                'id': get_user.id,
                'have_personal_area': get_user.have_personal_area
            })
            res.set_cookie('token', user.token, max_age=60*60)
            return res
        return jsonify({'error': 'Incorrect username or password'}), 401
    return jsonify({'error': 'User not found'}), 401


@authorization.route('/<provider>', methods=['GET'])
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@authorization.route('/callback/<provider>', methods=['GET'])
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        return jsonify({'error': 'Auth error'}), 401
    user_social = User_social.query.filter_by(social_id=social_id).first()
    if not user_social:
        token = str(uuid.uuid4())
        hash_password = generate_password_hash(username, method='sha256')
        create_user = User(username=username, password=hash_password, token=token)
        db.session.add(create_user)
        db.session.flush()
        id = create_user.id

        user_social = User_social(social_id=social_id, id_user=id)
        db.session.add(user_social)

        db.session.commit()
    get_user = User.query.filter(User.id == user_social.id_user).one()
    res = make_response({
        'id': get_user.id,
        'have_personal_area': get_user.have_personal_area
    })
    res.set_cookie('token', get_user.token, max_age=60 * 60)
    return res


@authorization.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    if data['username'] != '' and data['password'] != '':
        user = db.session.query(User).filter_by(username=data['username']).first()
        if not user:
            hash_password = generate_password_hash(data['password'], method='sha256')
            token = str(uuid.uuid4())
            create_user = User(username=data['username'], password=hash_password, token=token)
            db.session.add(create_user)
            db.session.flush()
            db.session.commit()
            return jsonify({'message': 'register successfully!'}), 201
        return jsonify({'error': 'User is already registered'}), 200
    return jsonify({'error': 'Empty fields'}), 400


@authorization.route('/logout', methods=['GET'])
@token_check
def logout(token):
    res = make_response("You are logout")
    res.set_cookie('token', token, max_age=0)
    return res

