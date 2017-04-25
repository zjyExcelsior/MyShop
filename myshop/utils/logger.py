# coding: utf-8
"""Logger Module"""

import logging
import logging.handlers
import os


def get_filehandler(log_dir, name, max_bytes, backup_count, fmt, datefmt, level=logging.DEBUG):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    filename = '%s.log' % name
    logger_file = os.path.join(log_dir, filename)
    file_handler = logging.handlers.RotatingFileHandler(
        logger_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    return file_handler
