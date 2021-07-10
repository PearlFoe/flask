from flask import (
	Blueprint,
	request,
	abort,
	redirect,
	url_for,
	session,
	render_template,
)
from flask_login import login_required

from app.database import db
from app.auth.models import User
from .models import Task
from .forms import InputTaskForm

module = Blueprint('user', __name__, url_prefix='/user/')

@module.route('/<user_id>/', methods=['GET'])
@login_required
def user(user_id=None):
	data = db.session.query(Task).filter(Task.user_id == user_id).all()
	login = db.session.query(User).filter(User.id == user_id).first().login

	return render_template('user/user.html', user=login, task=data, length=len(data))

@module.route('/<user_id>/<task_id>/', methods=['GET', 'POST'])
@login_required
def edit_task(user_id=None, task_id=None):
	user = db.session.query(User).filter(User.id == user_id).first()
	task = None

	if not db.session.query(db.exists().where(Task.id==task_id)).scalar():
		return 404
	else:
		task = db.session.query(Task).filter(Task.user_id == user_id).first()

	form = InputTaskForm()
	if form.validate_on_submit():
		if task_id:
			task.name = form.task_name.data
			task.description = form.task_description.data
		else:
			task = Task(
				name = form.task_name.data,
				description = form.task_description.data,
				user_id = user_id
			)

		db.session.add(task)
		db.session.commit()
		return redirect(url_for('user.user', user_id=user.id))

	return render_template('user/task.html', form=form, user=user.login, task=task)

@module.route('/<user_id>/new/', methods=['GET', 'POST'])
@login_required
def create_task(user_id=None):
	user = db.session.query(User).filter(User.id == user_id).first()
	form = InputTaskForm()
	task = None

	if form.validate_on_submit():
		task = Task(
			name = form.task_name.data,
			description = form.task_description.data,
			user_id = user_id
		)

		db.session.add(task)
		db.session.commit()

		return redirect(url_for('user.user', user_id=user.id))

	return render_template('user/task.html', form=form, user=user.login, task=task)
