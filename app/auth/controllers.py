from flask import (
	Blueprint,
	request,
	abort,
	redirect,
	url_for,
	session,
	render_template,
)
from flask_login import current_user, login_user, logout_user

from app.database import db
from .models import User
from .forms import LoginForm, RegisterForm

module = Blueprint('auth', __name__)

@module.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	message = None

	if current_user.is_authenticated:
		return redirect(url_for('user.user', user_id=current_user.id))

	if form.validate_on_submit():	
		login = form.login.data
		password = form.password.data

		user = db.session.query(User).filter(User.login == login).first()
		if not user or not user.check_password(password):
			message = "Incorrect login or password"
			return render_template('auth/login.html', message=message)

		login_user(user)
		return redirect(url_for('user.user', user_id=user.id))

	return render_template('auth/login.html', message=message, form=form)

@module.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@module.route('/registration', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	message = None
	if form.validate_on_submit():	
		username = form.username.data
		login = form.login.data
		password = form.password.data

		user = db.session.query(User).filter(User.login == login).first()
		if not user:
			user = User(
				name=username,
				login=login,
				password=User.set_password(password)
			)
			db.session.add(user) 
			db.session.commit()

			login_user(user)
			return redirect(url_for('user.user', user_id=user.id))
		else:
			message = 'Such login already exists.\nPlease change login and try again'

	return render_template('auth/sign_up.html', message=message, form=form)
