from app.models import db
import app.controller.utils as utils


definition = {
    'types': {
        'name': [str],
        'description': [str, type(None)]
    },
    'required': ['name'],
    'unique': ['name']
}


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    items = db.relationship('Item', backref='category', lazy=True)

    def to_dict(self) -> dict:
        obj = {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
        return obj

    def from_dict(self, data: dict, new: bool = False):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_data(data: dict, new: bool = False):
        error = utils.check_data(data, definition, new)
        return error
