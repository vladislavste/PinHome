from celery import Celery
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
celery = Celery()


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    celery.config_from_object(app.config)
    db.create_all(app)

