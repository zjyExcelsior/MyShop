# coding: utf-8
from flask import Blueprint, current_app, url_for
from ..models import User, Role
from ..ext import db

test = Blueprint('test', __name__)


@test.route('/test_remove_user/')
def test_remove_user():
    user = User.query.get(3)
    db.session.delete(user)
    db.session.commit()
    return 'yes'


@test.route('/test_session/')
def test_session():
    raise Exception(session.get('color_1'))


@test.route('/teststatic/')
def teststatic():
    return url_for('static', filename='image/logo.png')


@test.route('/testsql/')
def testsql():
    role = Role.query.filter(Role.id == 1).first()
    if role:
        db.session.delete(role)
        db.session.commit()
        return 'success'
    return 'there is no role'


@test.route('/test_log/')
def test_log():
    current_app.logger.info('test_log')
    return 'log success'
