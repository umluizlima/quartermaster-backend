from app.model import db
import app.controller.utils as utils


definition = {
    'types': {
        'first_name': [str],
        'last_name': [str],
        'email': [str],
        'phone': [str]
    },
    'required': ['first_name', 'last_name', 'email'],
    'unique': ['email']
}


class Thirdparty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    reservations = db.relationship(
        'Reservation',
        backref='thirdparty',
        lazy=True
    )
    lendings = db.relationship(
        'Lending',
        backref='thirdparty',
        lazy=True
    )

    def to_dict(self):
        obj = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone
        }
        return obj

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'email', 'phone']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_data(data: dict, new: bool = False):
        error = utils.check_data(data, definition, new) \
            or utils.check_name(data, 'first_name') \
            or utils.check_name(data, 'last_name') \
            or utils.check_email(data, 'email') \
            or utils.check_phone(data, 'phone')
        return error
