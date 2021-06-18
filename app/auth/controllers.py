from flask import (
	Blueprint,
	request,
	abort,
	redirect,
	url_for,
	session,
	render_template,
)
from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)

from app.database import db
from .models import User, Session
from .forms import LoginForm, RegisterForm

import app.utils as utils

module = Blueprint('auth', __name__)

@module.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	message = None

	if 'session_id' in session:
		session_exists = db.session.query(db.exists().where(Session.session_id==session['session_id'])).scalar()
		if session_exists:
			session_data = db.session.\
				query(Session).\
				filter(Session.session_id == session['session_id']).\
				first()

			new_session_id = utils.generate_key(30)
			session_data.session_id = new_session_id

			db.session.add(session_data) 
			db.session.commit()

			session['session_id'] = new_session_id
			session.modified = True

			return redirect(url_for('user.user', user_id=session_data.user_id))

	if form.validate_on_submit():	
		login = form.login.data
		password = form.password.data

		user_data = db.session.query(User).filter(User.login == login).first()
		if not user_data:
			message = "Incorrect login or password"
			return render_template('auth/login.html', message=message)

		user_password = user_data.password
		if not check_password_hash(user_password, password):
			message = "Incorrect login or password"
			return render_template('auth/login.html', message=message)

		session_exists = db.session.query(db.exists().where(Session.user_id==user_data.id)).scalar()
		if session_exists:
			session_data = db.session.\
							query(Session).\
							filter(Session.user_id == user_data.id).\
							first()

			user_id = session_data.user_id
			new_session_id = utils.generate_key(30)

			session_data.session_id = new_session_id
			db.session.add(session_data) 
			db.session.commit()

			session['session_id'] = new_session_id
			session.modified = True
		else:
			new_session_id = utils.generate_key(30)
			session_data = Session(
				user_id=user_data.id, 
				session_id=utils.new_session_id
				)

			db.session.add(session_data) 
			db.session.commit()

			session['session_id'] = new_session_id
			session.modified = True

		return redirect(url_for('user.user', user_id=user_data.id))

	return render_template('auth/login.html', message=message, form=form)

@module.route('/registration', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	message = None
	if form.validate_on_submit():	
		username = form.username.data
		login = form.login.data
		password = form.password.data

		user_exists = db.session.query(User).filter(User.login == login).first()
		if not user_exists:
			if (len(username) > 1) and (len(login) > 6) and (len(password) > 6):
				new_user = User(
					name=username,
					is_admin=0,
					login=login,
					password=generate_password_hash(password)
					)
				db.session.add(new_user) 
				db.session.commit()

				return redirect(url_for('user', user_id=user_id))
			else:
				message = 'Incorrect data length'
		else:
			message = 'Such login already exists.\nPlease change login and try again'

	return render_template('auth/sign_up.html', message=message, form=form)
