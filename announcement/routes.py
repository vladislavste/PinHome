import json
import os
from uuid import uuid4
from flask import Blueprint
from flask import current_app
from flask import request
from werkzeug.utils import secure_filename
from helpers import allowed_file
from .schema import AnnouncementSchema, AnnouncementImageSchema, CategorySchema
from ext import db
from .models import Announcement, ImagesAnnoun, Category
from authorization.authorization import token_check
from authorization.models import User
home_api = Blueprint('api', __name__)


@home_api.route('/create_annotation', methods=['POST'])
@token_check
def create_announcement(token):
    files = request.files.getlist('files')
    data = json.loads(request.form['request'])

    announcement_schema = AnnouncementSchema()
    image_schema = AnnouncementImageSchema()
    getted_user = User.query.filter(User.token == token).one()

    data['user'] = getted_user.id

    announcement = announcement_schema.load(data)

    db.session.add(announcement)
    db.session.flush()
    id = announcement.id
    db.session.commit()

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.split()[-1]
            new_filename = "upload-{}.{}".format(
                uuid4(), extension
            )

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER_ANNOUN'], new_filename))
            img_data = {
                "image_path": f'/images/uploads_annoum/{new_filename}',
                "announcement": id
            }
            db_image = image_schema.load(img_data)
            db.session.add(db_image)
            db.session.commit()

    return {
               "result": True
           }, 200


@home_api.route('/update_annotation/<id>', methods=['POST'])
@token_check
def update_annotation(token, id):
    files = request.files.getlist('files')
    data = json.loads(request.form['request'])
    image_schema = AnnouncementImageSchema()
    getted_user = User.query.filter(User.token == token).one()

    data['user'] = getted_user.id
    announcement = Announcement.query.get(id)

    if data.get('name'):
        announcement.name = data['name']
    if data.get('description'):
        announcement.description = data['description']
    if data.get('saled'):
        announcement.saled = data['saled']
    if data.get('category'):
        announcement.category = data['category']

    db.session.add(announcement)
    db.session.commit()

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.split()[-1]
            new_filename = "upload-{}.{}".format(
                uuid4(), extension
            )

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER_ANNOUN'], new_filename))
            img_data = {
                "image_path": f'/images/uploads_annoum/{new_filename}',
                "announcement": id
            }
            db_image = image_schema.load(img_data)
            db.session.add(db_image)
            db.session.commit()

    return {
               "result": True
           }, 200


@home_api.route('/delete_img_annotation/<id>', methods=['POST'])
@token_check
def delete_img_annotation(token, id):
    try:
        image_path = request.json['image_path']
    except KeyError:
        return {
                   "result": False
               }, 500
    db.session.query(ImagesAnnoun).filter(ImagesAnnoun.announcement == id).filter(ImagesAnnoun.image_path == image_path).delete()
    db.session.commit()

    full_path = current_app.config['PROJECT_HOME'] + image_path

    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print("The file does not exist")

    return {
               "result": True
           }, 200


@home_api.route('/delete_annotation/<id>', methods=['POST'])
@token_check
def delete_annotation(token, id):
    announcement = Announcement.query.get(id)
    announcement.deleted = True
    db.session.add(announcement)
    db.session.commit()
    return {
               "result": True
           }, 200

@home_api.route('/my_announcements/all_active', methods=['POST'])
@token_check
def all_announcements(token):
    getted_user = User.query.filter(User.token == token).one()
    all_announ = Announcement.query.filter(Announcement.user == getted_user.id, Announcement.deleted == False, Announcement.saled  == False).all()
    announcement_schema = AnnouncementSchema()
    all = announcement_schema.dump(all_announ, many=True)

    return {"announcement": all}, 200

@home_api.route('/my_announcements/deleted', methods=['POST'])
@token_check
def deleted_announcements(token):
    getted_user = User.query.filter(User.token == token).one()
    all_announ = Announcement.query.filter(Announcement.user == getted_user.id, Announcement.deleted == True).all()
    announcement_schema = AnnouncementSchema()
    all = announcement_schema.dump(all_announ, many=True)

    return {"announcement": all}, 200


@home_api.route('/my_announcements/saled', methods=['POST'])
@token_check
def saled_announcements(token):
    getted_user = User.query.filter(User.token == token).one()
    all_announ = Announcement.query.filter(Announcement.user == getted_user.id, Announcement.saled == True).all()
    announcement_schema = AnnouncementSchema()
    all = announcement_schema.dump(all_announ, many=True)

    return {"announcement": all}, 200

@home_api.route('/search_announcements', methods=['GET'])
def search_announcements():
    if request.args.get('category'):
        all_announs = Announcement.query.filter(Announcement.name.ilike('%' + request.args.get('query') + '%'), Announcement.category == request.args.get('category')).filter().all()
        announcement_schema = AnnouncementSchema()
        all = announcement_schema.dump(all_announs, many=True)
        return {"announcement": all}, 200
    else:
        all_announs = Announcement.query.filter(Announcement.name.ilike('%'+request.args.get('query')+'%')).all()
        announcement_schema = AnnouncementSchema()
        all = announcement_schema.dump(all_announs, many=True)
        return {"announcement": all}, 200


@home_api.route('/all_categories', methods=['GET'])
def all_categories():
    query = Category.query.all()
    category_schema = CategorySchema()
    all = category_schema.dump(query, many=True)
    return {"category": all}, 200


@home_api.route('/get_announcement/<id>', methods=['GET'])
def get_announcement(id):
    announ = Announcement.query.get(id)
    announcement_schema = AnnouncementSchema()
    all = announcement_schema.dump(announ)
    return all, 200

