from flask import (
    Blueprint,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy.exc import SQLAlchemyError

from app.database import db

module = Blueprint('comment', __name__, url_prefix='/comment')

@module.route('/', methods=['GET'])
def index():
    return 'test message'