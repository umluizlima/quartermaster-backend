"""Data model for thirdparties.

This module declares the Thirdparty class and its attributes.

"""

from app.model import db


class Thirdparty(db.Model):
    """Data model for thirdparties."""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reservations = db.relationship('Reservation',
                                   backref='thirdparty',
                                   lazy=True)
    lendings = db.relationship('Lending',
                               backref='thirdparty',
                               lazy=True)

    def to_dict(self):
        """Return a Thirdparty object formatted as dict."""
        obj = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        return obj

    def from_dict(self, data):
        """Fill Thirdparty attributes from given dictionary."""
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])
