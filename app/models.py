from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    job_title = db.Column(db.String(254))

    def __repr__(self):
        return '<Доктор {}>'.format(self.username)