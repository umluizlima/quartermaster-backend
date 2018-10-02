"""
Data model for lendings.

Every lending has a name, begin, end and return dates.
"""

from datetime import datetime as dt
from app.model import db
import app.controller.utils as utils

# def format_datetime(string):
#     return dt.strftime(string, '%Y-%m-%dT%H:%M')
#
#
# def parse_datetime(datetime):
#     return dt.strptime(datetime, '%Y-%m-%dT%H:%M')


definition = {
    'types': {
        'date_start': [str],
        'date_end': [str],
        'date_return': [str, type(None)],
        'item_id': [int, type(None)],
        'user_id': [int, type(None)],
        'thirdparty_id': [int, type(None)]
    },
    'required': ['date_start', 'date_end'],
    'unique': []
}


class Lending(db.Model):
    """Data model for lendings."""

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, nullable=False,
                           default=dt.utcnow)
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
            "date_start": self.date_start.isoformat(timespec='minutes'),
            "date_end": self.date_end.isoformat(timespec='minutes'),
            "date_return": self.date_return,
            "user_id": self.user_id,
            "thirdparty_id": self.thirdparty_id
        }
        if self.date_return:
            obj['date_return'] = self.date_return.isoformat(timespec='minutes')
        else:
            obj['date_return'] = None
        return obj

    def from_dict(self, data):
        """Fill Lending attributes from given dictionary."""
        for field in ['date_start', 'date_end', 'date_return', 'item_id',
                      'user_id', 'thirdparty_id']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_data(data: dict, new: bool = False):
        error = utils.check_data(data, definition, new) \
            or utils.check_datetime(data, 'date_start') \
            or utils.check_datetime(data, 'date_end') \
            or utils.check_datetime(data, 'date_return')
        if 'date_start' in data \
                and 'date_end' in data \
                and data['date_end'] <= data['date_start']:
            error = 'date_start deve ser menor que date_end'
        if 'date_start' in data \
                and 'date_return' in data \
                and data['date_return'] is not None \
                and data['date_return'] <= data['date_start']:
            error = 'date_start deve ser menor que date_return'
        return error
