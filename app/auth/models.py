from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)
from flask_login import (
	LoginManager, 
	UserMixin, 
	login_required
)

from app import login_manager
from app.database import db


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(45), nullable=False)
	login = db.Column(db.String(45), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	api_key = db.Column(db.String(80))

	def __str__(self):
		return self.name

	def set_password(password):
		return generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))