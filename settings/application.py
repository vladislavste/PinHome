from flask import Flask
from flask_cors import CORS
from authorization.views import authorization
from settings.configuration import Config
from ext import register_extensions
from announcement.routes import home_api

def create_application():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    register_extensions(app)

    app.register_blueprint(authorization, url_prefix='/authorization')
    app.register_blueprint(home_api, url_prefix='/api')

    return app
