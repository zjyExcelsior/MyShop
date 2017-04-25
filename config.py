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
LOGGER_NAME = 'myshop' # Flask's app logger name
LOG_DIR = os.path.join(_basedir, 'logs')
LOG_LEVEL = logging.INFO
FILE_HANDLER_LEVEL = logging.DEBUG
LOG_MAX_BYTES = 1024 * 1024 * 10
LOG_BACKUP_COUNT = 5
LOG_FMT = '%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s() %(levelname)s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'


DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# myshop configs
BEST_SELLER_DISPLAY_COUNT = 3 # 首页热销商品展示数量

try:
    from local_settings import *  # 导入本地配置
except ImportError:
    pass

del os
