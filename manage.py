from app import create_app
from app.database import db

import os

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])


if __name__ == '__main__':
	manager.run()