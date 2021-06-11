from flask import (
	Blueprint,
	request,
	abort,
	redirect,
	url_for,
	session
)
from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)

from app.database import db
from .models import User, Session
from .utils import 

module = Blueprint('auth', __name__)

@module.route('/', methods=['GET', 'POST'])
def login():
	if 'session_id' in session:
		session_exists = db.session.query(exists().where(Session.field==session['session_id'])).scalar()
		if session_exists:
			session_data = db.session.\
				query(Session).\
				filter(Session.session_id == session['session_id']).\
				first()

			user_id = session_data.user_id

			session_data.session_id = utils.generate_key(30)
			session.add(session_data) 
			session.commit()

			return redirect(url_for('user', user_id=user_id))

	message = None
	if request.method == 'POST':
		login = request.form.get('login')
		password = request.form.get('password')

		if not password or not login:
			message = "Incorrect login or password"
			return render_template('login.html', message=message)

		user_data = db.session.query(User).filter(User.login == login).first()
		if not data:
			message = "Incorrect login or password"
			return render_template('login.html', message=message)

		user_password = user_data.password
		if not check_password_hash(user)
			message = "Incorrect login or password"
			return render_template('login.html', message=message)

		session_exists = db.session.query(exists().where(Session.user_id==user_data.id)).scalar()
		if session_exists:
			session_data = db.session.\
				query(Session).\
				filter(Session.user_id == user_data.id).\
				first()

			user_id = session_data.user_id

			session_data.session_id = utils.generate_key(30)
			session.add(session_data) 
			session.commit()
		else:
			session_data = Session(
				user_id=user_data.id, 
				session_id=utils.generate_key(30)
				)
			session.add(session_data) 
			session.commit()


		return redirect(url_for('user', user_id=user_id))


	return render_template('login.html', message=message)

@module.route('/registration', methods=['GET', 'POST'])
def register():
	return 'registration test message'
