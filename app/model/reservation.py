"""
Data model for reservations.

Every reservation has a name, begin, and end dates.
"""

import re
from datetime import datetime
from app.model import db, User, Thirdparty


class Reservation(db.Model):
    """Data model for reservations."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id',
                                      onupdate='CASCADE',
                                      ondelete='SET NULL'),
                        nullable=True)
    thirdparty_id = db.Column(db.Integer,
                              db.ForeignKey('thirdparty.id',
                                            onupdate='CASCADE',
                                            ondelete='SET NULL'),
                              nullable=True)

    def to_dict(self):
        """Return a Reservation object formatted as dict."""
        obj = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "user_id": self.user_id,
            "thirdparty_id": self.thirdparty_id
        }
        return obj

    def from_dict(self, data):
        """Fill Reservation attributes from given dictionary."""
        for field in ['name', 'description', 'date_start', 'date_end',
                      'user_id', 'thirdparty_id']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_data(data: dict, new: bool = False):
        """Verify Reservation data for correct keys and types."""
        # Check if data is empty.
        if len(data.keys()) == 0:
            return 'empty request'
        # Check if data contains any unexpected keys.
        all_keys = ['name', 'description', 'date_start',
                    'date_end', 'user_id', 'thirdparty_id']
        if any([key not in all_keys for key in data.keys()]):
            return 'invalid attributes'

        # Check if data contains all required keys for new lending.
        required_keys = ['name', 'date_start', 'date_end',
                         'user_id', 'thirdparty_id']
        if new and any([key not in data.keys() for key in required_keys]):
            return 'missing required attributes'

        # Validate each present key.
        if 'name' in data:
            # Check for type.
            if type(data['name']) is not str:
                return 'name must be string'
            # Check for expected regex pattern.
            name = re.compile(r'\w+( \w+)*')
            if re.fullmatch(name, data['name']) is None:
                return 'invalid name'

        if 'description' in data:
            # Check for type.
            if type(data['description']) is not str and \
                    data['description'] is not None:
                return 'description must be string or null'
            # Check for expected regex pattern.
            # description = re.compile(r'')
            # if re.fullmatch(description, data['description']) is None:
            #     return 'invalid description'

        # if 'available' in data:
        #     # Check for type.
        #     if type(data['available']) is not bool:
        #         return 'available must be bool'
        #
        if 'user_id' in data:
            # Check for type.
            if type(data['user_id']) is not int and \
                    data['user_id'] is not None:
                return 'user id must be int or null'
            # Check for existance.
            if type(data['user_id']) is int and \
                    User.query.get(data['user_id']) is None:
                return 'invalid user_id'

        if 'thirdparty_id' in data:
            # Check for type.
            if type(data['thirdparty_id']) is not int and \
                    data['thirdparty_id'] is not None:
                return 'thirdparty id must be int or null'
            # Check for existance.
            if type(data['thirdparty_id']) is int and \
                    Thirdparty.query.get(data['thirdparty_id']) is None:
                return 'invalid thirdparty_id'

        # if 'registry' in data:
        #     # Check for type.
        #     if type(data['registry']) is not str and \
        #             data['registry'] is not None:
        #         return 'registry must be string or null'

        return None
