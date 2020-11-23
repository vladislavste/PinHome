from flask import Flask
from flask_cors import CORS
from authorization.views import authorization
from settings.configuration import Config
from ext import register_extensions
from announcement.routes import home_api
from personal_area.views import personal_area
from charities.views import charities
from chat.views import chat
from about_service.views import about_service
from support.views import support
from reference.views import reference


def create_application():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    register_extensions(app)

    app.register_blueprint(authorization, url_prefix='/authorization')
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(personal_area, url_prefix='/personal_area')
    app.register_blueprint(charities, url_prefix='/charities')
    app.register_blueprint(chat, url_prefix='/chat')
    app.register_blueprint(about_service, url_prefix='/about_service')
    app.register_blueprint(support, url_prefix='/support')
    app.register_blueprint(reference, url_prefix='/reference')

    return app
