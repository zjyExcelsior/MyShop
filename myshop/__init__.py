# coding: utf-8
from flask import Flask
from .ext import db, migrate, login_manager, admin, api, cache, toolbar
from .utils.logger import get_filehandler
import logging


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    # app.logger
    log_dir = app.config.get('LOG_DIR')
    log_level = app.config.get('FILE_LOG_LEVEL')
    app.logger.addHandler(get_filehandler(log_dir, 'web', level=log_level))
    app.logger.setLevel(app.config.get('LOG_LEVEL'))

    # 配置extensions
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db=db)
    admin.init_app(app)
    api.init_app(app)
    cache.init_app(app)
    toolbar.init_app(app)

    # 导入视图，注册蓝图
    from .views.main import main
    from .views.auth import auth
    from .views.restful import restful
    from .views.test import test
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)
    app.register_blueprint(restful)

    return app
