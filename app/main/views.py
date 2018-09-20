from datetime import datetime, date, timedelta

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from numpy import is_busday

from config import Config
from . import main
from .forms import AddEmployeForm, EditEmployeForm
from .forms import AddHolidayForm, EditHolidayForm
from .forms import AddPatientForm, EditPatientForm
from .forms import AddSicklistForm, EditSicklistForm, CloseListForm
from .forms import CheckinForm
from .. import db
from ..models import User, Patients, Lists, Employes, Holiday


@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit = datetime.utcnow()
        db.session.commit()


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    today = date.today()
    sicklists = Lists.query.filter_by(
        status='open',
        first_checkin=today,
        first_checkin_fact=None).order_by(Lists.start_date.desc()).all()
    sicklists += Lists.query.filter_by(
        status='open',
        second_checkin=today,
        second_checkin_fact=None).order_by(Lists.start_date.desc()).all()
    sicklists += Lists.query.filter_by(
        status='open',
        vkk=today,
        vkk_fact=None).order_by(Lists.start_date.desc()).all()
    return render_template('index.html', title='Главная', header='Совместные осмотры сегодня', sicklists=sicklists,
                           today=today)


@main.route('/all')
@login_required
def all():
    today = date.today()
    sicklists = Lists.query.order_by(Lists.start_date.desc()).all()
    return render_template('index.html', title='Все б/л', header='Список больничных листов', sicklists=sicklists,
                           today=today)


@main.route('/list_employes')
@login_required
def list_employes():
    employes = Employes.query.outerjoin(User, (
                User.employe_id == Employes.id)).add_columns(
                    Employes.id,
                    Employes.last_name,
                    Employes.first_name,
                    Employes.middle_name,
                    Employes.job_title,
                    User.username).order_by(
                        Employes.last_name).all()
    return render_template('employes.html', title='Сотрудники', employes=employes)


@main.route('/add_employe', methods=['GET', 'POST'])
@login_required
def add_employe():
    form = AddEmployeForm()
    if form.validate_on_submit():
        employe = Employes(last_name=form.last_name.data,
                           first_name=form.first_name.data,
                           middle_name=form.middle_name.data,
                           job_title=form.job_title.data)
        db.session.add(employe)
        db.session.commit()
        flash('Сотрудник {} {} {} добавлен'.format(form.last_name.data, form.first_name.data, form.middle_name.data))
        return redirect(url_for('main.add_employe'))
    return render_template('add_employe.html', title='Добавление сотрудника', form=form)


@main.route('/edit_employe/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employe(id):
    employe = Employes.query.filter_by(id=id).first_or_404()
    form = EditEmployeForm()
    if form.validate_on_submit():
        Employes.query.filter_by(id=int(form.id.data)).update(
                                    {'last_name': form.last_name.data,
                                     'first_name': form.first_name.data,
                                     'middle_name': form.middle_name.data,
                                     'job_title': form.job_title.data})
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('main.edit_employe', id=form.id.data))
    elif request.method == 'GET':
        form.id.data = employe.id
        form.last_name.data = employe.last_name
        form.first_name.data = employe.first_name
        form.middle_name.data = employe.middle_name
        form.job_title.data = employe.job_title
    return render_template('edit_employe.html', title='Редактирование сотрудника', form=form)


@main.route('/employe/<int:id>')
@login_required
def employe(id):
    employe = Employes.query.filter_by(id=id).first_or_404()
    lists = Lists.query.filter_by(doctor_id=id).all()
    return render_template('employe.html', employe=employe, lists=lists)


@main.route('/list_patients')
@login_required
def list_patients():
    patients = Patients.query.order_by(Patients.last_name).all()
    return render_template('list_patients.html', patients=patients)


@main.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = Patients(last_name=form.last_name.data,
                           first_name=form.first_name.data,
                           middle_name=form.middle_name.data,
                           birth_year=form.birth_year.data,
                           sex=request.form['sex'])
        db.session.add(patient)
        db.session.commit()
        flash('Пациент {} {} {} {} года рождения, добавлен'.format(
                                    form.last_name.data,
                                    form.first_name.data,
                                    form.middle_name.data,
                                    form.birth_year.data))
        return redirect(url_for('main.add_patient'))
    return render_template('add_patient.html', title='Добавление пациента', form=form)


@main.route('/patient/<int:id>')
@login_required
def patient(id):
    patient = Patients.query.filter_by(id=id).first_or_404()
    return render_template('patient.html', patient=patient)


@main.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patients.query.filter_by(id=id).first_or_404()
    form = EditPatientForm(obj=patient)
    if form.validate_on_submit():
        Patients.query.filter_by(id=int(form.id.data)).update(
                                    {'last_name': form.last_name.data,
                                     'first_name': form.first_name.data,
                                     'middle_name': form.middle_name.data,
                                     'birth_year': form.birth_year.data,
                                     'sex': request.form['sex']})
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('main.edit_patient', id=form.id.data))
    elif request.method == 'GET':
        form.id.data = patient.id
        form.last_name.data = patient.last_name
        form.first_name.data = patient.first_name
        form.middle_name.data = patient.middle_name
        form.birth_year.data = patient.birth_year
        form.sex.default = patient.sex
    return render_template('edit_patient.html', form=form, patient=patient)


def is_work_day(checkinday, holiday):
    while not is_busday(checkinday, weekmask=Config.WORK_DAYS, holidays=holiday):
        checkinday = checkinday - timedelta(days=1)
    return checkinday


@main.route('/add_sicklist', methods=['GET', 'POST'])
@login_required
def add_sicklist():
    form = AddSicklistForm()
    form.patient.choices = [(p.id, " ".join([p.last_name, p.first_name, p.middle_name]))
                                for p in Patients.query.order_by('last_name')]
    form.doctor.choices = [(e.id, " ".join([e.last_name, e.first_name, e.middle_name]))
                                for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        first_checkin_date = form.start_date.data + timedelta(days=9)
        first_checkin_date = is_work_day(first_checkin_date, Holiday.list_holidays())
        second_checkin_date = first_checkin_date + timedelta(days=10)
        second_checkin_date = is_work_day(second_checkin_date, Holiday.list_holidays())
        vkk_date = second_checkin_date + timedelta(days=10)
        vkk_date = is_work_day(vkk_date, Holiday.list_holidays())
        sicklist = Lists(sick_list_number=form.sick_list_number.data,
                         start_date=form.start_date.data,
                         doctor_who_open_list=request.form['doctor'],
                         first_checkin=first_checkin_date,
                         second_checkin=second_checkin_date,
                         vkk=vkk_date,
                         status=request.form['status'],
                         diacrisis=form.diacrisis.data,
                         patient_id=request.form['patient'],
                         doctor_id=request.form['doctor'])
        db.session.add(sicklist)
        db.session.commit()
        flash('Больничный лист № {} добавлен'.format(form.sick_list_number.data))
        return redirect(url_for('main.add_sicklist'))
    return render_template('add_sicklist.html', title='Добавление нового больничного листа', form=form)


@main.route('/edit_list/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_list(id):
    sicklist = Lists.query.filter_by(id=id).first_or_404()
    form = EditSicklistForm(obj=sicklist)
    form.patient.choices = [(p.id, p.last_name + ' ' + p.first_name + ' ' + p.middle_name)
                                for p in Patients.query.order_by('last_name')]
    form.doctor.choices = [(e.id, e.last_name + ' ' + e.first_name + ' ' + e.middle_name)
                                for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        first_checkin_date = form.start_date.data + timedelta(days=9)
        first_checkin_date = is_work_day(first_checkin_date, Holiday.list_holidays())
        if sicklist.first_checkin_fact:
            second_checkin_date = sicklist.first_checkin_fact + timedelta(days=10)
            second_checkin_date = is_work_day(second_checkin_date, Holiday.list_holidays())
        else:
            second_checkin_date = first_checkin_date + timedelta(days=10)
            second_checkin_date = is_work_day(second_checkin_date, Holiday.list_holidays())
        if sicklist.second_checkin_fact:
            vkk_date = sicklist.second_checkin_fact + timedelta(days=10)
            vkk_date = is_work_day(vkk_date, Holiday.list_holidays())
        else:
            vkk_date = second_checkin_date + timedelta(days=10)
            vkk_date = is_work_day(vkk_date, Holiday.list_holidays())

        Lists.query.filter_by(id=int(form.id.data)).update(
                               {'sick_list_number': form.sick_list_number.data,
                                'start_date': form.start_date.data,
                                'status': request.form['status'],
                                'status_note': form.status_note.data,
                                'diacrisis': form.diacrisis.data,
                                'patient_id': request.form['patient'],
                                'doctor_id': request.form['doctor'],
                                'first_checkin': first_checkin_date,
                                'second_checkin': second_checkin_date,
                                'vkk': vkk_date})
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('main.edit_list', id = form.id.data))
    elif request.method == 'GET':
        form.status.default = sicklist.status
        form.patient.default = sicklist.patient.id
        form.doctor.default = sicklist.doctor.id
        form.process()
        form.id.data = sicklist.id
        form.sick_list_number.data = sicklist.sick_list_number
        form.start_date.data = sicklist.start_date
        form.diacrisis.data = sicklist.diacrisis
        form.status_note.data = sicklist.status_note
    return render_template('edit_list.html', form=form, sicklist=sicklist)


@main.route('/close_list/<int:id>', methods=['GET', 'POST'])
@login_required
def close_list(id):
    sicklist = Lists.query.filter_by(id=id).first_or_404()
    form = CloseListForm()
    if form.validate_on_submit():
        Lists.query.filter_by(id=int(form.id.data)).update(
                               {'end_date': form.end_date.data,
                                'status_note': form.status_note.data,
                                'status': 'end'})
        db.session.commit()
        flash('Больничный лист № {} закрыт'.format(sicklist.sick_list_number))
        return redirect(url_for('main.edit_list', id=form.id.data))
    elif request.method == 'GET':
        form.id.data = sicklist.id
        form.end_date.data = sicklist.end_date
    return render_template('close_list.html', form=form, sicklist=sicklist)


@main.route('/list_holidays')
@login_required
def list_holidays():
    holidays = Holiday.query.order_by(Holiday.holiday_date.desc()).all()
    return render_template('list_holidays.html', holidays=holidays)


@main.route('/add_holiday', methods=['GET', 'POST'])
@login_required
def add_holiday():
    form = AddHolidayForm()
    if form.validate_on_submit():
        year = form.holiday_date.data.year
        holiday = Holiday(holiday_year=year,
                          holiday_date=form.holiday_date.data,
                          holiday_name=form.holiday_name.data)
        db.session.add(holiday)
        db.session.commit()
        flash('Выходной {} добавлен'.format(form.holiday_date.data))
        return redirect(url_for('main.add_holiday'))
    return render_template('add_holiday.html',
                           form=form,
                           title='Добавить выходной')


@main.route('/edit_holiday/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_holiday(id):
    holiday = Holiday.query.filter_by(id=id).first_or_404()
    form = EditHolidayForm()
    if form.validate_on_submit():
        year = form.holiday_date.data.year
        Holiday.query.filter_by(id=int(form.id.data)).update(
                       {'holiday_year': year,
                        'holiday_date': form.holiday_date.data,
                        'holiday_name': form.holiday_name.data})
        db.session.commit()
        flash('Выходной {} добавлен'.format(form.holiday_date.data))
        return redirect(url_for('main.list_holidays'))
    elif request.method == 'GET':
        form.id.data = holiday.id
        form.holiday_date.data = holiday.holiday_date
        form.holiday_name.data = holiday.holiday_name
    return render_template('holiday.html',
                           form=form,
                           holiday=holiday,
                           title='Редактировать выходной')


@main.route('/del_holiday/<int:id>')
@login_required
def del_holiday(id):
    holiday = Holiday.query.filter_by(id=id).first_or_404()
    db.session.delete(holiday)
    db.session.commit()
    flash(f'Выходной {holiday.holiday_date} {holiday.holiday_name}, удалён.')
    return redirect(url_for('main.list_holidays'))


@main.route('/add_checkin/<int:id>/<type_checkin>', methods=['GET', 'POST'])
@login_required
def add_checkin(id, type_checkin):
    form = CheckinForm()
    if form.validate_on_submit():
        if type_checkin == 'first':
            second_checkin_date = form.checkin_date.data + timedelta(days=10)
            second_checkin_date = is_work_day(second_checkin_date, Holiday.list_holidays())
            vkk_date = second_checkin_date + timedelta(days=10)
            vkk_date = is_work_day(vkk_date, Holiday.list_holidays())
            Lists.query.filter_by(id=int(form.id.data)).update(
                            {'first_checkin_fact': form.checkin_date.data,
                             'first_checkin_note': form.checkin_note.data,
                             'second_checkin': second_checkin_date,
                             'vkk': vkk_date})
        elif type_checkin == 'second':
            vkk_date = form.checkin_date.data + timedelta(days=10)
            vkk_date = is_work_day(vkk_date, Holiday.list_holidays())
            Lists.query.filter_by(id=int(form.id.data)).update(
                            {'second_checkin_fact': form.checkin_date.data,
                             'second_checkin_note': form.checkin_note.data,
                             'vkk': vkk_date})
        elif type_checkin == 'vkk':
            Lists.query.filter_by(id=int(form.id.data)).update(
                            {'vkk_checkin_fact': form.checkin_date.data,
                             'vkk_checkin_note': form.checkin_note.data})
        db.session.commit()
        flash('Совместный осмотр {} добавлен'.format(form.checkin_date.data))
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.id.data = id
    return render_template('checkin.html',
                           form=form,
                           title='Добавить совместный осмотр')


@main.route('/edit_checkin/<int:id>/<type_checkin>', methods=['GET', 'POST'])
@login_required
def edit_checkin(id, type_checkin):
    form = CheckinForm()
    if form.validate_on_submit():
        if type_checkin == 'first':
            second_checkin_date = form.checkin_date.data + timedelta(days=10)
            second_checkin_date = is_work_day(second_checkin_date, Holiday.list_holidays())
            vkk_date = second_checkin_date + timedelta(days=10)
            vkk_date = is_work_day(vkk_date, Holiday.list_holidays())
            Lists.query.filter_by(id=int(form.id.data)).update(
                            {'first_checkin_fact': form.checkin_date.data,
                             'first_checkin_note': form.checkin_note.data,
                             'second_checkin': second_checkin_date,
                             'vkk': vkk_date})
        elif type_checkin == 'second':
            vkk_date = form.checkin_date.data + timedelta(days=10)
            vkk_date = is_work_day(vkk_date, Holiday.list_holidays())
            Lists.query.filter_by(id=int(form.id.data)).update(
                            {'second_checkin_fact': form.checkin_date.data,
                             'second_checkin_note': form.checkin_note.data,
                             'vkk': vkk_date})
        elif type_checkin == 'vkk':
            Lists.query.filter_by(id=int(form.id.data)).update(
                            {'vkk_checkin_fact': form.checkin_date.data,
                             'vkk_checkin_note': form.checkin_note.data})
        db.session.commit()
        flash('Совместный осмотр {} изменён'.format(form.checkin_date.data))
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        checkins_list = Lists.query.filter_by(id=int(id)).first_or_404()
        form.id.data = id
        if type_checkin == 'first':
            form.checkin_date.data = checkins_list.first_checkin_fact
            form.checkin_note.data = checkins_list.first_checkin_note
        elif type_checkin == 'second':
            form.checkin_date.data = checkins_list.second_checkin_fact
            form.checkin_note.data = checkins_list.second_checkin_note
        elif type_checkin == 'vkk':
            form.checkin_date.data = checkins_list.vkk_fact
            form.checkin_note.data = checkins_list.vkk_note
    return render_template('checkin.html',
                           form=form,
                           title='Добавить совместный осмотр')
