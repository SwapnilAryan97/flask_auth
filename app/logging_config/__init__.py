import logging
from logging.config import dictConfig

import flask
from flask import request, current_app, blueprints

from app.logging_config.log_formatters import RequestFormatter

log_con = flask.Blueprint('log_con', __name__)


@log_con.before_app_request
def before_request_logging():
    current_app.logger.info("Before Request")
    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("myDebug")
    log.debug("My Debug Logger Message")


@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response
    current_app.logger.info("After Request")

    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("myDebug")
    log.debug("My Debug Logger Message")
    return response


@log_con.before_app_first_request
def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("myDebug")
    log.debug("My Debug Logger Message")


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'RequestFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '[%(asctime)s] [%(process)d] %(remote_addr)s requested %(url)s'
                      '%(levelname)s in %(module)s: %(message)s'
        },
        'DebugFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '%(levelname)s : %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler.myApp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'RequestFormatter',
            # 'filename': 'app/logs/myinfo.log',
            'filename': os.path.join(config.Config.LOG_DIR, 'myApp.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myDebug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'DebugFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'myDebug.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'myApp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myApp'],
            'level': 'INFO',
            'propagate': False
        },
        'myDebug': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myDebug'],
            'level': 'DEBUG',
            'propagate': False
        }

    }
}