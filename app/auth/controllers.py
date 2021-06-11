from flask import (
	Blueprint,
	request,
	flash,
	abort,
	redirect,
	url_for,
	current_app,
	session
)
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from .models import User

module = Blueprint('auth', __name__)

@module.route('/', methods=['GET', 'POST'])
def login():
	return 'test message'

@module.route('/registration', methods=['GET', 'POST'])
def register():
	pass
