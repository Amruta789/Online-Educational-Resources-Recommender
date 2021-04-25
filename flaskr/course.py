# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 16:38:30 2021

@author: Amruta
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import mongo

bp = Blueprint('course', __name__)

@bp.route('/')
def index():
    courses = mongo.db.courses.find()
    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            mongo.db.courses.insert_one({'title': title, 'body': body, 'lecturer_id':g.user['_id']})
            return redirect(url_for('course.index'))

    return render_template('course/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            course = mongo.db.courses.find_one_and_replace({'_id': id}, {'title': title, 'body': body},{'upsert':False})

            return redirect(url_for('course.index'))

    return render_template('course/update.html', course=course)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    course = mongo.db.course.delete_one({'_id': courseId})
    return redirect(url_for('course.index'))