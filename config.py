import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    COURSES_PER_PAGE = 10
    UPLOADS_DEFAULT_DEST=os.path.join(basedir, 'instance/uploads')
    #UPLOADED_FILES_ALLOW=tuple('jfif')
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'instance/final.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') # localhost or smtp.googlemail.com
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) # 8025 or 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None # 1 (when using gmail, otherwise don't specify)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # your-email-address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # your-email-password
    ADMINS = ['imtech2k18@gmail.com']
    GOOGLE_YOUTUBE_API_KEY = os.environ.get('GOOGLE_YOUTUBE_API_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')