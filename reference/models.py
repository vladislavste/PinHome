from ext import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Reference(db.Model):
    __tablename__ = 'reference'
    id = db.Column(db.Integer, primary_key=True)
    charities = relationship("Charities", backref="charities")
    support = relationship("Support", backref="cupport")
    about_service = relationship("About_service", backref="about_service")

