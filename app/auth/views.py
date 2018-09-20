from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import User, Employes
from .forms import LoginForm, RegistrationForm, EditProfileForm
from werkzeug.urls import url_parse
from datetime import datetime


@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit = datetime.utcnow()
        db.session.commit()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя или пароль')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Войти', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.username != 'Admin':
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    form.employe.choices = [(e.id, e.last_name + ' ' + e.first_name + ' ' + e.middle_name)
                                for e in Employes.query.order_by('last_name')]
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, employe_id=request.form['employe'])
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь {} добавлен'.format(form.username.data))
        return redirect(url_for('auth.register'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@auth.route('/del_user/<int:id>')
@login_required
def del_user(id):
    if current_user.username != 'Admin':
        return redirect(url_for('main.index'))
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь {} удалён'.format(user.username))
    return redirect(url_for('auth.list_users'))


@auth.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    employe = Employes.query.filter_by(id=user.employe_id).first()
    return render_template('auth/user.html', user=user, employe=employe)


@auth.route('/list_users')
@login_required
def list_users():
    users = User.query.order_by(User.username).all()
    return render_template('auth/list_users.html', users=users)


@auth.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.edit_profile', id=form.id.data))
    elif request.method == 'GET':
        form.employe.default = user.employe_id
        form.process()
        form.id.data = user.id
        form.username.data = user.username
        form.email.data = user.email
    return render_template('auth/edit_profile.html',
                           title='Редактирование профиля пользователя',
                           form=form,
                           user=user)

