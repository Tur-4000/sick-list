from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Employes, Lists


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
    id = HiddenField('id')
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
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    middle_name = StringField('Отчество')
    job_title = StringField('Должность')
    submit = SubmitField('Сохранить')


class AddPatientForm(FlaskForm):
    id = HiddenField('id')
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[DataRequired()])
    birth_year = StringField('Год рождения', validators=[DataRequired()])
    sex = SelectField('Пол', choices=[('man', 'Мужской'), ('woman', 'Женский')])
    submit = SubmitField('Сохранить')

class EditPatientForm(FlaskForm):
    id = HiddenField('id')
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[DataRequired()])
    birth_year = StringField('Год рождения', validators=[DataRequired()])
    sex = SelectField('Пол', choices=[('man', 'Мужской'), ('woman', 'Женский')], coerce=str)
    submit = SubmitField('Сохранить')


class AddSicklistForm(FlaskForm):
    id = HiddenField('id')
    sick_list_number = StringField('Номер больничного', validators=[DataRequired()],
                                    render_kw={'placeholder': 'Номер больничного'})
    start_date = DateField('Дата открытия', format='%Y-%m-%d', validators=[DataRequired()])
    patient = SelectField('Пациент', coerce=int)
    diacrisis = StringField('Диагноз', validators=[DataRequired()])
    doctor = SelectField('Лечащий врач', coerce=int)
    status = SelectField('Статус', choices=[('open', 'Открыт'), ('end', 'Закрыт'), ('relocated', 'перемещён')], coerce=str)
    submit = SubmitField('Сохранить')

    def validate_sick_list_number(self, sick_list_number):
        number = Lists.query.filter_by(sick_list_number=sick_list_number.data).first()
        if number is not None:
            raise ValidationError('Больничный с таким номером уже есть в базе')

class EditSicklistForm(FlaskForm):
    id = HiddenField('id')
    sick_list_number = StringField('Номер больничного', validators=[DataRequired()])
    start_date = DateField('Дата открытия', format='%Y-%m-%d', validators=[DataRequired()])
    patient = SelectField('Пациент', coerce=int)
    diacrisis = StringField('Диагноз', validators=[DataRequired()])
    doctor = SelectField('Лечащий врач', coerce=int)
    status = SelectField('Статус', choices=[('open', 'Открыт'), ('end', 'Закрыт'), ('relocated', 'перемещён')], coerce=str)
    submit = SubmitField('Сохранить')
    
class CloseListForm(FlaskForm):
    id = HiddenField('id')
    end_date = DateField('Дата закрытия больничного', validators=[DataRequired()])
    submit = SubmitField('Закрыть больничный')