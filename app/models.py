from app import db
from datetime import datetime


class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)

    def __repr__(self):
        return f'<Temp {self.datetime} {self.temperature}>'
