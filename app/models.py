from app import app, db
from datetime import datetime
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
    sick_lists = db.relationship('Lists', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Доктор {}>'.format(self.username)


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    birth_year = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    sick_lists = db.relationship('Lists', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Пациент {}>'.format(self.last_name)


class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sick_list_number = db.Column(db.String(32))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(32))
    diacrisis = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))

    def __repr__(self):
        return '<Больничный лист № {}>'.format(self.sick_list_number)