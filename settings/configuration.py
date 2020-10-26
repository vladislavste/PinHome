import os


class Config:
    DEBUG = False
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = 'postgres://kshcgzkjxlfwdc:2a105932715ec1b6732b6ab9204b252544d03aaceff10005f28512a68e30a9f4@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/d7vc1htmtmq5fa'
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:2452020@localhost:5432/pinhome'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROJECT_HOME = os.path.dirname(os.path.realpath(__file__)).replace('/settings', '')
    UPLOAD_FOLDER_ANNOUN = '{}/images/announcement/'.format(PROJECT_HOME)
    UPLOAD_FOLDER_PERSONAL_AREA = '{}/images/personal_area/'.format(PROJECT_HOME)
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'png"', 'jpg"', 'jpeg"'])
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '649881479030378',
            'secret': '32b05f9979c1a1bb7632e31f216e38cb'
        }
    }