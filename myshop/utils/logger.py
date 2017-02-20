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

def get_filehandler(log_dir, name, level=logging.DEBUG):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    filename = '%s.log' % name
    logger_file = os.path.join(log_dir, filename)
    file_handler = logging.handlers.RotatingFileHandler(
        logger_file, maxBytes=LOG_MAX, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(LOG_FORMAT)
    file_handler.setLevel(level)
    return file_handler
