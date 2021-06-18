from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
	login = StringField(validators=[DataRequired()], render_kw={"placeholder": "Login"})
	password = PasswordField(validators=[DataRequired(), Length(min=6, max=80)], render_kw={"placeholder": "Password"})
	submit_btn = SubmitField('Log in')

class RegisterForm(FlaskForm):
	username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Username"})
	login = StringField(validators=[DataRequired()], render_kw={"placeholder": "Login"})
	password = PasswordField(validators=[DataRequired(), Length(min=6, max=80)], render_kw={"placeholder": "Password"})
	submit_btn = SubmitField('Register')