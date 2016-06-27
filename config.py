import os
import logging

SECRET_KEY = '123456'
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/myshop'
SQLALCHEMY_TRACK_MODIFICATIONS = True
LOG_DIR = os.path.join(os.getcwd(), 'logs')
FILE_LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
