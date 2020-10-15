from ext import db


class Personal_area(db.Model):
    __tablename__ = 'personal_area'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True, unique=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    geolocation = db.Column(db.String(200), nullable=True)
    #photo =
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    def __init__(self, surname=None, name=None, patronymic=None,
                 phone_number=None, email=None, geolocation=None,
                 id_user=None):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.phone_number = phone_number
        self.email = email
        self.geolocation = geolocation
        #self.photo = photo
        self.id_user = id_user