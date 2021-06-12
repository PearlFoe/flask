from app.database import db
from app.auth.models import User

class Tasks(db.Model):
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(45), nullable=False)
	description = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey(User.id))

	def __str__(self):
		return self.name