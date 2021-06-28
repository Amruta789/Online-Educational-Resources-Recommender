import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'instance/TeachAid.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False