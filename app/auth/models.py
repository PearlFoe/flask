from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Varchar(45), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    login = db.Column(db.Varchar(45), nullable=False)
    password = db.Column(db.Varchar(80), nullable=False)
    api_key = db.Column(db.Varchar(80))

    def __str__(self):
        return self.name
