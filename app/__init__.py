import os
from flask import Flask

from .database import db

def create_app():
	app = Flask(__name__)
	app.config.from_object(os.environ['APP_SETTINGS'])
	app.permanent_session_lifetime = datetime.timedelta(days=1)

	db.init_app(app)

	import app.auth.controllers as auth
	import app.user.controllers as user

	app.register_blueprint(auth.module)
	app.register_blueprint(user.module) 

	return app