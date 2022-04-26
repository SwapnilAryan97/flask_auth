import os

class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = '***Insecure! Dont use this in production!***'
    SESSION_COOKIE_SECURE = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'Simplex'
    DB_DIR = ''