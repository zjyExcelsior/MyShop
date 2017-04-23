# coding: utf-8
import os
import logging

_basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '123456'

# Flask-SQLAlchemy configs
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'myshop'
SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(MYSQL_USER,
                                                                            MYSQL_PASSWD,
                                                                            MYSQL_HOST,
                                                                            MYSQL_PORT,
                                                                            MYSQL_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# log configs
LOG_DIR = os.path.join(_basedir, 'logs')
FILE_LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

try:
    from local_settings import *  # 导入本地配置
except ImportError:
    pass

del os
