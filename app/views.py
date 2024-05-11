from flask import Blueprint, render_template, request
from app.models import eat

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Adjust the number of items per page as needed
    eats = eat.query.order_by(eat.date_added.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', eats=eats)
