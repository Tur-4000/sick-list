from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Employes

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    employe = SelectField('Сотрудник', coerce=int)
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторить пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Добавить')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя пользователя')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой email')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя')
    email = StringField('eMail')
    employe = SelectField('Сотрудник', coerce=int)
    submit = SubmitField('Сохранить')


class AddEmployeForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    job_title = StringField('Должность', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class EditEmployeForm(FlaskForm):
    id = HiddenField('id')
    last_name = StringField('Имя')
    first_name = StringField('Фамилия')
    middle_name = StringField('Отчество')
    job_title = StringField('Должность')
    submit = SubmitField('Сохранить')