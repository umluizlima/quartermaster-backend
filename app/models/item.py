from app.models import db
import app.controller.utils as utils


definition = {
    'types': {
        'registry': [str, type(None)],
        'name': [str],
        'description': [str, type(None)],
        'available': [bool],
        'category_id': [int, type(None)],
    },
    'required': ['name'],
    'unique': ['registry']
}


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registry = db.Column(db.String(32), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id',
                                          onupdate='CASCADE',
                                          ondelete='SET NULL'),
                            nullable=True)
    lendings = db.relationship('Lending', backref='item', lazy=True)

    def to_dict(self):
        obj = {
            "id": self.id,
            "registry": self.registry,
            "name": self.name,
            "description": self.description,
            "available": self.available,
            "category_id": self.category_id
        }
        return obj

    def from_dict(self, data):
        for field in ['registry', 'name', 'description', 'category_id',
                      'available']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_data(data: dict, new: bool = False):
        error = utils.check_data(data, definition, new)
        return error
