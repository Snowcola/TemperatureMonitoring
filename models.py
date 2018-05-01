from fridge import db


class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True, unique=True)
    temperature = db.Column(db.Float)

    def __repr__(self):
        return f'<Temp {self.datetime} {self.temperature}>'
