from flask_wtf import FlaskForm
from wtforms import StringField, TextField

class InputTaskForm(FlaskForm):
	task_name = StringField('Title')
	task_description = TextField('Description')