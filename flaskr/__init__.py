# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:39:20 2021

@author: Amruta
"""
import os

import flask
from .db import mongo

def create_app(test_config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI='mongodb://localhost:27017/courses',
    )
    mongo.init_app(app)
    
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
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import course
    app.register_blueprint(course.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route("/")
    def home():
        courses = mongo.db.courses.find()
        return flask.jsonify([course for course in courses])
    
    @app.route("/get_course/<int:courseId>")
    def get_one(courseId):
        course = mongo.db.courses.find_one({"_id": courseId})
        return course

    @app.route("/add_one", methods=('GET', 'POST'))
    def add_one():
        mongo.db.courses.insert_one({'title': "Course Name", 'body': "Course body"})
        return flask.jsonify(message="success")
    
    @app.route("/replace_course/<int:courseId>", methods=('GET', 'POST'))
    def replace_one(courseId):
        course = mongo.db.courses.find_one_and_replace({'_id': courseId}, {'title': "modified title"},{'upsert':False})
        return course
    
    @app.route("/delete_course/<int:courseId>", methods=['DELETE'])
    def delete_course(courseId):
        course = mongo.db.course.delete_one({'_id': courseId})
        return course.raw_result

    return app