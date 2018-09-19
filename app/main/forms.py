from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Length
from ..models import Lists, Holiday


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
    birth_year = DateField('Дата рождения', validators=[DataRequired()])
    sex = SelectField('Пол', choices=[('0', 'Мужской'), ('1', 'Женский')])
    submit = SubmitField('Сохранить')


class EditPatientForm(FlaskForm):
    id = HiddenField('id')
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[DataRequired()])
    birth_year = DateField('Дата рождения', validators=[DataRequired()])
    sex = SelectField('Пол', choices=[('0', 'Мужской'), ('1', 'Женский')], coerce=str)
    submit = SubmitField('Сохранить')


class AddSicklistForm(FlaskForm):
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
    status_note = TextAreaField('Примечание', validators=[Length(min=0, max=255)])
    submit = SubmitField('Сохранить')


class CloseListForm(FlaskForm):
    id = HiddenField('id')
    end_date = DateField('Дата закрытия больничного', validators=[DataRequired()])
    status_note = TextAreaField('Примечание', validators=[Length(min=0, max=255)])
    submit = SubmitField('Закрыть больничный')


class AddHolidayForm(FlaskForm):
    holiday_date = DateField('Дата выходного', validators=[DataRequired()])
    holiday_name = StringField('Описание', validators=[DataRequired()],
                                    render_kw={'placeholder': 'Описание'})
    submit = SubmitField('Сохранить')

    def validate_holiday_date(self, holiday_date):
        hdate = Holiday.query.filter_by(holiday_date=holiday_date.data).first()
        if hdate is not None:
            raise ValidationError('Выходной на эту дату уже есть в базе')


class EditHolidayForm(FlaskForm):
    id = HiddenField('id')
    holiday_date = DateField('Дата выходного', validators=[DataRequired()])
    holiday_name = StringField('Описание', validators=[DataRequired()],
                                    render_kw={'placeholder': 'Описание'})
    submit = SubmitField('Сохранить')


class CheckinForm(FlaskForm):
    id = HiddenField('id')
    checkin_date = DateField('Дата совместного осмотра',
                             validators=[DataRequired()])
    checkin_note = TextAreaField('Описание',
                                 validators=[Length(min=0, max=255)],
                                 render_kw={'placeholder': 'Описание'})
    submit = SubmitField('Сохранить')
