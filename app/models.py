from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    employe_id = db.Column(db.Integer, db.ForeignKey('employes.id'))

    def __repr__(self):
        return '<Пользователь {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    job_title = db.Column(db.String(254))
    user = db.relationship('User', backref='user', lazy='dynamic')
    doctor = db.relationship('Lists', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Сотрудник: {} {} {}>'.format(self.last_name, self.first_name, self.middle_name)


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    birth_year = db.Column(db.Date)
    sex = db.Column(db.Integer)
    sick_lists = db.relationship('Lists', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Пациент {}>'.format(self.last_name)


class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sick_list_number = db.Column(db.String(32), index=True, unique=True)
    start_date = db.Column(db.Date)
    first_checkin = db.Column(db.Date)
    first_checkin_fact = db.Column(db.Date)
    first_checkin_note = db.Column(db.String(255))
    second_checkin = db.Column(db.Date)
    second_checkin_fact = db.Column(db.Date)
    second_checkin_note = db.Column(db.String(255))
    vkk = db.Column(db.Date)
    vkk_fact = db.Column(db.Date)
    vkk_note = db.Column(db.String(255))
    end_date = db.Column(db.Date)
    status = db.Column(db.String(32))
    diacrisis = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('employes.id'))

    def __repr__(self):
        return '<Больничный лист № {}>'.format(self.sick_list_number)


class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    holiday_year = db.Column(db.Integer)
    holiday_date = db.Column(db.Date, index=True, unique=True)
    holiday_name = db.Column(db.String(128))

    def __repr__(self):
        return '<{} - {}>'.format(self.holiday_date, self.holiday_name)
