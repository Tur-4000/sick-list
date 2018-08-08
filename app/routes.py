from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.forms import AddEmployeForm, EditEmployeForm
from app.forms import AddPatientForm, EditPatientForm
from app.forms import AddSicklistForm, EditSicklistForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Patients, Lists, Employes
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sicklists = Lists.query.order_by(Lists.start_date).all()
    return render_template('index.html', title='Главная', header='Совместные осмотры сегодня', sicklists=sicklists)

@app.route('/all')
@login_required
def all():
    sicklists = Lists.query.order_by(Lists.start_date).all()
    return render_template('index.html', title='Все б/л', header='Список больничных листов', sicklists=sicklists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.username != 'Admin':
        return redirect(url_for('index'))
    form = RegistrationForm()
    form.employe.choices = [(e.id, e.last_name + ' ' + e.first_name + ' ' + e.middle_name) 
                                for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, employe_id=request.form['employe'])
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь {} добавлен'.format(form.username.data))
        return redirect(url_for('register'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/del_user/<id>')
@login_required
def del_user(id):
    if current_user.username != 'Admin':
        return redirect(url_for('index'))
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь {} удалён'.format(user.username))
    return redirect(url_for('list_users'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    employe = Employes.query.filter_by(id=user.employe_id).first()
    return render_template('user.html', user=user, employe=employe)

@app.route('/list_users')
@login_required
def list_users():
    users = User.query.order_by(User.username).all()
    return render_template('list_users.html', users=users)


@app.route('/edit_profile/<id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = EditProfileForm(obj=user)
    form.employe.choices = [(e.id, e.last_name + ' ' + e.first_name + ' ' + e.middle_name)
                                    for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.employe_id = request.form['employe']
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile', id=form.id.data))
    elif request.method == 'GET':
        form.employe.default = user.employe_id
        form.process()
        form.id.data = user.id
        form.username.data = user.username
        form.email.data = user.email
    return render_template('edit_profile.html', title='Редактирование профиля пользователя', form=form, user=user)


@app.route('/list_employes')
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

@app.route('/add_employe', methods=['GET', 'POST'])
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
        flash('Сотрудник {} добавлен'.format(form.last_name.data))
        return redirect(url_for('add_employe'))
    return render_template('add_employe.html', title='Добавление сотрудника', form=form)

@app.route('/edit_employe/<id>', methods=['GET', 'POST'])
@login_required
def edit_employe(id):
    employe = Employes.query.filter_by(id=id).first_or_404()
    form = EditEmployeForm()
    if form.validate_on_submit():
        employe = Employes.query.filter_by(id=int(form.id.data)).update(
                                        {'last_name': form.last_name.data, 
                                         'first_name': form.first_name.data,
                                         'middle_name': form.middle_name.data,
                                         'job_title': form.job_title.data})
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_employe', id = form.id.data))
    elif request.method == 'GET':
        form.id.data = employe.id
        form.last_name.data = employe.last_name
        form.first_name.data = employe.first_name
        form.middle_name.data = employe.middle_name
        form.job_title.data = employe.job_title
    return render_template('edit_employe.html', title='Редактирование сотрудника', form=form)

@app.route('/employe/<id>')
@login_required
def employe(id):
    employe = Employes.query.filter_by(id=id).first_or_404()
    return render_template('employe.html', employe=employe)

@app.route('/list_patients')
@login_required
def list_patients():
    patients = Patients.query.order_by(Patients.last_name).all()
    return render_template('list_patients.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
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
        return redirect(url_for('add_patient'))
    return render_template('add_patient.html', title='Добавление пациента', form=form)

@app.route('/patient/<id>')
@login_required
def patient(id):
    patient = Patients.query.filter_by(id=id).first_or_404()
    return render_template('patient.html', patient=patient)

@app.route('/edit_patient/<id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patients.query.filter_by(id=id).first_or_404()
    form = EditPatientForm(obj=patient)
    if form.validate_on_submit():
        patients = Patients.query.filter_by(id=int(form.id.data)).update(
                                        {'last_name': form.last_name.data, 
                                         'first_name': form.first_name.data,
                                         'middle_name': form.middle_name.data,
                                         'birth_year': form.birth_year.data,
                                         'sex': request.form['sex']})
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_patient', id = form.id.data))
    elif request.method == 'GET':
        form.id.data = patient.id
        form.last_name.data = patient.last_name
        form.first_name.data = patient.first_name
        form.middle_name.data = patient.middle_name
        form.birth_year.data = patient.birth_year
        form.sex.default = patient.sex
    return render_template('edit_patient.html', form=form, patient=patient)


@app.route('/add_sicklist', methods=['GET', 'POST'])
@login_required
def add_sicklist():
    form = AddSicklistForm()
    form.patient.choices = [(p.id, p.last_name + ' ' + p.first_name + ' ' + p.middle_name) 
                                for p in Patients.query.order_by('last_name')]
    form.doctor.choices = [(e.id, e.last_name + ' ' + e.first_name + ' ' + e.middle_name) 
                                for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        sicklist = Lists(sick_list_number=form.sick_list_number.data, 
                         start_date=form.start_date.data,
                         status=request.form['status'],
                         diacrisis=form.diacrisis.data,
                         patient_id=request.form['patient'], 
                         doctor_id = request.form['doctor'])
        db.session.add(sicklist)
        db.session.commit()
        flash('Больничный лист № {} добавлен'.format(form.sick_list_number.data))
        return redirect(url_for('add_sicklist'))
    return render_template('add_sicklist.html', title='Добавление нового больничного листа', form=form)

@app.route('/edit_list/<id>', methods=['GET', 'POST'])
@login_required
def edit_list(id):
    sicklist = Lists.query.filter_by(id=id).first_or_404()
    form = EditSicklistForm(obj=sicklist)
    form.patient.choices = [(p.id, p.last_name + ' ' + p.first_name + ' ' + p.middle_name) 
                                for p in Patients.query.order_by('last_name')]
    form.doctor.choices = [(e.id, e.last_name + ' ' + e.first_name + ' ' + e.middle_name) 
                                for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        Lists.query.filter_by(id=int(form.id.data)).update(
                               {'sick_list_number': form.sick_list_number.data,
                                'start_date': form.start_date.data,
                                'status': request.form['status'],
                                'diacrisis': form.diacrisis.data,
                                'patient_id': request.form['patient'],
                                'doctor_id': request.form['doctor']})
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_list', id = form.id.data))
    elif request.method == 'GET':
        form.status.default = sicklist.status
        form.patient.default = sicklist.patient.id
        form.doctor.default = sicklist.doctor.id
        form.process()
        form.id.data = sicklist.id
        form.sick_list_number.data = sicklist.sick_list_number
        form.start_date.data = sicklist.start_date
        form.diacrisis.data = sicklist.diacrisis
    return render_template('edit_list.html', form=form, sicklist=sicklist)
