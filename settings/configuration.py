import os


class Config:
    DEBUG = False
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = 'postgres://pinhome:23kP6Zu@localhost:5432/pinhome'
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:2452020@localhost:5432/pinhome'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROJECT_HOME = os.path.dirname(os.path.realpath(__file__)).replace('/settings', '')
    UPLOAD_FOLDER_ANNOUN = '{}/images/announcement/'.format(PROJECT_HOME)
    UPLOAD_FOLDER_PERSONAL_AREA = '{}/images/personal_area/'.format(PROJECT_HOME)
    UPLOAD_FOLDER_CHARITIES = '{}/images/charities/'.format(PROJECT_HOME)
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'png"', 'jpg"', 'jpeg"'])
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '649881479030378',
            'secret': '32b05f9979c1a1bb7632e31f216e38cb'
        },
        'google': {
            'id': '157583496567-p15f3jnijg9oe9d29erpveomb58mr4n0.apps.googleusercontent.com',
            'secret': 'O_piVp3zrWtJCI1bv29ohmRA'
        },
        'yandex': {
            'id': '52e6d831ff30406aa6d6000e127d1cde',
            'secret': '749bec84b7c8436b899998a665b66f1c'
        }
    }
    SECRET_KEY = 'lolkekazaza'