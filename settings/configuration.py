import os


class Config:
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://pinhouse:pinhouse@localhost:5432/pinhouse'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:2452020@localhost:5432/pinhome'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROJECT_HOME = os.path.dirname(os.path.realpath(__file__)).replace('/settings', '')
    UPLOAD_FOLDER_ANNOUN = '{}/images/uploads_annoum/'.format(PROJECT_HOME)
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'png"', 'jpg"', 'jpeg"'])
