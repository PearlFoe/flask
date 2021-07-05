from app import create_app
from app.database import db

from flask_script import Manager
from flask_bootstrap import Bootstrap

import os

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)
bootstrap = Bootstrap(app)

#python manage.py runserver
#'mysql+pymysql://root:pass@localhost/my_db'

if __name__ == '__main__':
	manager.run()