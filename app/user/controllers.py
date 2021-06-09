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

module = Blueprint('user', __name__, url_prefix='/user/')

@module.route('/<login>', methods=['GET'])
def user(login=None):
	return f"user {login}"