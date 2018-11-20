from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={'placeholder': 'Имя пользователя'})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={'placeholder': 'Пароль'})
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    employe = SelectField('Сотрудник', coerce=int)
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторить пароль',
                              validators=[DataRequired(), EqualTo('password')])
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
    id = HiddenField('id')
    username = StringField('Имя пользователя')
    email = StringField('eMail')
    employe = SelectField('Сотрудник', coerce=int)
    role = SelectField('Права доступа', coerce=int)
    submit = SubmitField('Сохранить')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() and \
                (User.query.filter_by(username=field.data).first().username !=
                 field.data):
            raise ValidationError('Такой логин уже используется')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() and \
                (User.query.filter_by(email=field.data).first().email !=
                 field.data):
            raise ValidationError('Такой eMail уже зарегистрирован.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать.')])
    password2 = PasswordField('Подтверждение нового пароля',
                              validators=[DataRequired()])
    submit = SubmitField('Изменить пароль')


class ChangeEmailForm(FlaskForm):
    old_email = StringField('Старый eMail')
    new_email = StringField('Новый eMail')
    submit = SubmitField('Изменить eMail')

    # TODO: добавить валидацию email на уникальность
