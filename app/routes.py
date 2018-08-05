from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddEmployeForm, EditEmployeForm
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
    return render_template('index.html', title='Главная', sicklists=sicklists)


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
    if current_user.username != 'Tur':
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь {} добавлен'.format(form.username.data))
        return redirect(url_for('register'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@app.route('/list_employes')
@login_required
def list_employes():
    employes = Employes.query.order_by(Employes.last_name).all()
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
    form = EditEmployeForm()
    employe = Employes.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        # TODO: доделать сохранение
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