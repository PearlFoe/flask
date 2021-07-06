from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class InputTaskForm(FlaskForm):
	task_name = StringField('Title')
	task_description = TextAreaField('Description')
	submit_btn = SubmitField('Save')