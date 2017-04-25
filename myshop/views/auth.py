# coding: utf-8
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required
from ..forms import LoginForm, RegistrationForm
from ..models import User
from ..ext import db

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('main.index'))
        flash(u'密码错误')
    return render_template('auth/login.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('auth/signup.html', form=form)
