# coding: utf-8
'''
Logger Module
'''

import logging
import logging.handlers
import os

LOG_MAX = 1024 * 1024 * 10
BACKUP_COUNT = 5
LOG_FORMAT = logging.Formatter(
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')

def get_filehandler(name, level=logging.DEBUG):
    base_path = os.getcwd()
    logs_dir = os.path.join(base_path, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    filename = '%s.log' % name
    logger_file = os.path.join(logs_dir, filename)
    file_handler = logging.handlers.RotatingFileHandler(
        logger_file, maxBytes=LOG_MAX, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(LOG_FORMAT)
    file_handler.setLevel(level)
    return file_handler
