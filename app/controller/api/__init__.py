from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.controller.api import (
    thirdparties, categories, items)
