from flask import (
	Blueprint,
	request,
	abort,
	redirect,
	url_for,
	session,
	render_template,
)

from app.database import db
from app.auth.models import User, Session
from .models import Tasks
from .forms import InputTaskForm

module = Blueprint('user', __name__, url_prefix='/user/')

@module.route('/<user_id>', methods=['GET'])
def user(user_id=None):
	if 'session_id' in session:
		session_exists = db.session.query(db.exists().where(Session.session_id==session['session_id'])).scalar()
		if session_exists:
			data = db.session.query(Tasks).filter(Tasks.user_id == user_id).all()
			login = db.session.query(User).filter(User.id == user_id).first().login

			return render_template('user/user.html', user=login, tasks=data, length=len(data))
		
	return redirect(url_for('auth.login'))

@module.route('/<user_id>/<task_id>', methods=['GET', 'POST'])
def edit_task(user_id=None, task_id=None):
	login = None
	data = None
	form = InputTaskForm()

	return render_template('user/task.html', form=form, user=login, task=data)
