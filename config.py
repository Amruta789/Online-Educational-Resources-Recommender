import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    COURSES_PER_PAGE = 3
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'instance/site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['imtech2k18@gmail.com']