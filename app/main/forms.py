from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, \
    TextAreaField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Length
from ..models import Lists, Holiday, Patients, Employes, Diacrisis


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
    dismissed = BooleanField('Заблокировать')

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


class SicklistForm(FlaskForm):
    id = HiddenField('id')
    sick_list_number = StringField('Номер больничного', validators=[DataRequired()],
                                   render_kw={'placeholder': 'Номер больничного'})
    start_date = DateField('Дата открытия', format='%Y-%m-%d', validators=[DataRequired()])
    patient = SelectField('Пациент', coerce=int)
    diagnoses = SelectField('Диагноз', coerce=int)
    doctor = SelectField('Лечащий врач', coerce=int)
    status = SelectField('Статус', choices=[('open', 'Открыт'), ('relocated', 'перемещён')], coerce=str)
    status_note = TextAreaField('Примечание',
                                validators=[Length(min=0, max=255)])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(SicklistForm, self).__init__(*args, **kwargs)
        self.patient.choices = [(p.id, " ".join([p.last_name, p.first_name, p.middle_name]))
                                for p in Patients.query.order_by('last_name')]
        self.doctor.choices = [(e.id, " ".join([e.last_name, e.first_name, e.middle_name]))
                               for e in Employes.query.filter_by(dismissed=False).order_by('last_name')]
        self.diagnoses.choices = [(dia.id, dia.diagnoses)
                                  for dia in Diacrisis.query.order_by('diagnoses')]

    def validate_sick_list_number(self, field):
        if field.data != self.sick_list_number.data and \
                Lists.query.filter_by(sick_list_number=field.data).first():
            raise ValidationError('Больничный с таким номером уже есть в базе')


class CloseListForm(FlaskForm):
    id = HiddenField('id')
    end_date = DateField('Дата закрытия больничного',
                         validators=[DataRequired()])
    status_note = TextAreaField('Примечание',
                                validators=[Length(min=0, max=255)])
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


class DiacrisisForm(FlaskForm):
    id = HiddenField('id')
    diagnoses = StringField('Диагноз', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Сохранить')

    def validate_diagnoses(self, field):
        if field.data != self.diagnoses.data and \
                Diacrisis.query.filter_by(diagnoses=field.data).first():
            raise ValidationError('Такой диагноз уже есть в базе')


class SetScanLabelForm(FlaskForm):
    id = HiddenField('id')
    scan = BooleanField('Карточка отсканирована')
    submit = SubmitField('Сохранить')
