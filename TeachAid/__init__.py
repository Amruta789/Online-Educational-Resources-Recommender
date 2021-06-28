# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:39:20 2021

@author: Amruta
"""
import os

import flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'TeachAid.sqlite'),
    # )
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # from . import db
    # db.init_app(app)
    from . import models
    db.init_app(app)
    migrate.init_app(app, db)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import course
    app.register_blueprint(course.bp)
    app.add_url_rule('/', endpoint='index')

    return app
