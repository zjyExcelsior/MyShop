# coding: utf-8
from flask import Flask
from .ext import db, migrate, login_manager, admin, api, cache, toolbar
from .utils.logger import get_filehandler
import logging


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    # app.logger
    app_config = app.config
    log_dir = app_config.get('LOG_DIR')
    log_name = app_config.get('LOGGER_NAME')
    log_max_bytes = app_config.get('LOG_MAX_BYTES')
    log_backup_count = app_config.get('LOG_BACKUP_COUNT')
    fmt = app_config.get('LOG_FMT')
    datefmt = app_config.get('LOG_DATEFMT')
    file_handler_level = app_config.get('FILE_HANDLER_LEVEL')
    log_level = app_config.get('LOG_LEVEL')
    file_handler = get_filehandler(log_dir, log_name, log_max_bytes, log_backup_count, fmt, datefmt, file_handler_level)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)

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
    from .views.apis import apis
    from .views.test import test
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)
    app.register_blueprint(apis)

    return app
