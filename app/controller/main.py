from flask import (
    Blueprint, render_template
)
from app.controller.auth import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    """Render the main page."""
    return render_template('main/index.html', title="CDG Hub")
