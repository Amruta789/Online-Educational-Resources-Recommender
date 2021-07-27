# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:39:20 2021

@author: Amruta
"""
import os

import flask
from flask import send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import configure_uploads
from elasticsearch import Elasticsearch


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()

def create_app(test_config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/uploads/<path:filename>')
    def get_file(filename):
        return send_from_directory(app.config['UPLOADS_DEFAULT_DEST'],filename)
    
    from . import models
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    mail.init_app(app)
    from .user import profilephotos
    from .course import courseprofiles
    configure_uploads(app,(profilephotos,courseprofiles))

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import course
    app.register_blueprint(course.bp)

    from .import search
    app.register_blueprint(search.bp)

    from . import user
    app.register_blueprint(user.bp)
    app.add_url_rule('/', endpoint='index')

    return app
