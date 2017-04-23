# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_restful import Api
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
import os

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

admin = Admin(name='MyShop', template_mode='bootstrap3')
path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

api = Api()
cache = Cache(config={'CACHE_TYPE': 'simple'})
toolbar = DebugToolbarExtension()
