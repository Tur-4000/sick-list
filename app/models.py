from datetime import datetime, timedelta

from flask import current_app
from flask_login import UserMixin
from numpy import is_busday
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from . import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Permission:
    READ = 1
    WRITE = 2
    ADMIN = 4


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    employe_id = db.Column(db.Integer, db.ForeignKey('employes.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['SICKLIST_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<Пользователь {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


class Role(db.Model):
    """Пользовательские роли"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ, Permission.WRITE],
            'Administrator': [Permission.READ, Permission.WRITE,
                              Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    job_title = db.Column(db.String(254))
    dismissed = db.Column(db.Boolean, default=False, index=True)
    user = db.relationship('User', backref='user', lazy='dynamic')

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


def is_work_day(checkinday, holiday):
    while not is_busday(checkinday, weekmask=Config.WORK_DAYS, holidays=holiday):
        checkinday = checkinday - timedelta(days=1)
    return checkinday


class Lists(db.Model):
    """Модель больничных листов
    """
    id = db.Column(db.Integer, primary_key=True)
    sick_list_number = db.Column(db.String(32), index=True, unique=True)
    start_date = db.Column(db.Date)
    doctor_who_open_list = db.Column(db.Integer, db.ForeignKey('employes.id'))
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
    status_note = db.Column(db.String(255))
    diagnoses_id = db.Column(db.Integer, db.ForeignKey('diacrisis.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('employes.id'))
    doctor = db.relationship('Employes', foreign_keys=[doctor_id])
    open_list_doctor = db.relationship('Employes',
                                       foreign_keys=[doctor_who_open_list])
    scan_label = db.Column(db.Boolean, index=True, default=False)

    def __repr__(self):
        return '<Больничный лист № {}>'.format(self.sick_list_number)

    @staticmethod
    def on_set_start_date(target, value, oldvalue, initiator):
        """Расчёт плановых дат совместных осмотров
        """
        target.first_checkin = is_work_day((value + timedelta(days=9)),
                                           Holiday.list_holidays())
        second_checkin_date = target.first_checkin + timedelta(days=10)
        target.second_checkin = is_work_day(second_checkin_date,
                                            Holiday.list_holidays())
        vkk_date = target.second_checkin + timedelta(days=10)
        target.vkk = is_work_day(vkk_date, Holiday.list_holidays())

    # @staticmethod
    # def on_changed_first_checkin_fact(target, value, oldvalue, initiator):
    #     """Расчёт плановых дат совместных осмотров при установке фактической
    #        даты первого совместного осмотра
    #     """
    #     second_checkin_date = value + timedelta(days=10)
    #     target.second_checkin = is_work_day(second_checkin_date,
    #                                         Holiday.list_holidays())
    #     vkk_date = target.second_checkin + timedelta(days=10)
    #     target.vkk = is_work_day(vkk_date, Holiday.list_holidays())
    #
    # @staticmethod
    # def on_changed_second_checkin_fact(target, value, oldvalue, initiator):
    #     """Расчёт плановых дат совместных осмотров при установке фактической
    #        даты второго совместного осмотра
    #     """
    #     vkk_date = value + timedelta(days=10)
    #     target.vkk = is_work_day(vkk_date, Holiday.list_holidays())


db.event.listen(Lists.start_date, 'set', Lists.on_set_start_date)
# db.event.listen(Lists.first_checkin_fact, 'set', Lists.on_changed_first_checkin_fact)
# db.event.listen(Lists.second_checkin_fact, 'set', Lists.on_changed_second_checkin_fact)


class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    holiday_year = db.Column(db.Integer)
    holiday_date = db.Column(db.Date, index=True, unique=True)
    holiday_name = db.Column(db.String(128))

    def __repr__(self):
        return '<{} - {}>'.format(self.holiday_date, self.holiday_name)

    @staticmethod
    def list_holidays():
        holidays_dates = Holiday.query.with_entities(
            Holiday.holiday_date).all()
        holidays = []
        for date in holidays_dates:
            holidays += [date.holiday_date.strftime("%Y-%m-%d")]
        return holidays


class Diacrisis(db.Model):
    __tablename__ = 'diacrisis'
    id = db.Column(db.Integer, primary_key=True)
    diagnoses = db.Column(db.String(255), index=True, unique=True, nullable=False)
    sick_lists = db.relationship('Lists', backref='diacrisis', lazy='dynamic')

    def __repr__(self):
        return f'<{self.diagnoses}>'
