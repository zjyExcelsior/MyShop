# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_restful import Api
from flask_cache import Cache
import os.path as op
from .utils.logger import get_filehandler
import logging


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
db = SQLAlchemy()
admin = Admin(name='MyShop', template_mode='bootstrap3')
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
api = Api()
cache = Cache(config={'CACHE_TYPE': 'simple'})

from .views.main import main
from .views.auth import auth
from .views.restful import restful
from .views.test import test


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.logger.addHandler(get_filehandler(
        app.config.get('LOG_DIR'), 'web', level=app.config.get('FILE_LOG_LEVEL')))
    app.logger.setLevel(app.config.get('LOG_LEVEL'))
    login_manager.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    api.init_app(app)
    cache.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)
    app.register_blueprint(restful)
    return app
