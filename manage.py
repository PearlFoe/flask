from app import create_app
from app.database import db

from flask_script import Manager

import os

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)


if __name__ == '__main__':
	manager.run()