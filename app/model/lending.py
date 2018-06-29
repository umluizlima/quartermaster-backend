"""
Data model for lendings.

Every lending has a name, begin, end and return dates.
"""

from app.model import db
from datetime import datetime


class Lending(db.Model):
    """Data model for lendings."""

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    date_end = db.Column(db.DateTime, nullable=False)
    date_return = db.Column(db.DateTime, nullable=True)
    item_id = db.Column(db.Integer,
                        db.ForeignKey('item.id',
                                      onupdate='CASCADE',
                                      ondelete='SET NULL'),
                        nullable=True)
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
        """Return a Lending object formatted as dict."""
        obj = {
            "id": self.id,
            "item_id": self.item_id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "date_return": self.date_return,
            "user_id": self.user_id,
            "thirdparty_id": self.thirdparty_id
        }
        return obj

    def from_dict(self, data):
        """Fill Lending attributes from given dictionary."""
        for field in ['date_start', 'date_end', 'date_return', 'item_id',
                      'user_id', 'thirdparty_id']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_data(data: dict, new: bool = False):
        """Verify Lending data for correct keys and types."""
        # Check if data is empty.
        if len(data.keys()) == 0:
            return 'empty request'
        # Check if data contains any unexpected keys.
        all_keys = ['date_start', 'date_end', 'date_return',
                    'item_id', 'user_id', 'thirdparty_id']
        if any([key not in all_keys for key in data.keys()]):
            return 'invalid attributes'

        # Check if data contains all required keys for new lending.
        required_keys = ['date_start', 'date_end', 'item_id',
                         'user_id', 'thirdparty_id']
        if new and any([key not in data.keys() for key in required_keys]):
            return 'missing required attributes'

        # # Validate each present key.
        # if 'date_start' in data:
        #     # Check for type.
        #     if type(data['name']) is not str:
        #         return 'name must be string'
        #     # Check for expected regex pattern.
        #     name = re.compile(r'\w+( \w+)*')
        #     if re.fullmatch(name, data['name']) is None:
        #         return 'invalid name'
        #
        # if 'description' in data:
        #     # Check for type.
        #     if type(data['description']) is not str and \
        #             data['description'] is not None:
        #         return 'description must be string or null'
        #     # Check for expected regex pattern.
        #     # description = re.compile(r'')
        #     # if re.fullmatch(description, data['description']) is None:
        #     #     return 'invalid description'
        #
        # if 'available' in data:
        #     # Check for type.
        #     if type(data['available']) is not bool:
        #         return 'available must be bool'
        #
        # if 'category_id' in data:
        #     # Check for type.
        #     if type(data['category_id']) is not int and \
        #             data['category_id'] is not None:
        #         return 'category id must be int or null'
        #     # Check for existance.
        #     if type(data['category_id']) is int and \
        #             Category.query.get(data['category_id']) is None:
        #         return 'invalid category_id'
        #
        # if 'registry' in data:
        #     # Check for type.
        #     if type(data['registry']) is not str and \
        #             data['registry'] is not None:
        #         return 'registry must be string or null'

        return None
