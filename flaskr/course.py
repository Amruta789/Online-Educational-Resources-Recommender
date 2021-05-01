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
from flaskr.db import get_db

bp = Blueprint('course', __name__)

@bp.route('/')
def index():
    db = get_db()
    courses = db.execute(
        'SELECT c.id, title, body, created, lecturer_id, username'
        ' FROM course c JOIN user u ON c.lecturer_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
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
            db = get_db()
            db.execute(
                'INSERT INTO course (title, body, lecturer_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('course.index'))

    return render_template('course/create.html')

def get_course(id, check_lecturer=True):
    course = get_db().execute(
        'SELECT c.id, title, body, created, lecturer_id, username'
        ' FROM course c JOIN user u ON c.lecturer_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()
    if course is None:
        abort(404, "Course id {0} doesn't exist.".format(id))
    if check_lecturer and course['lecturer_id'] != g.user['id']:
        abort(403)
    return course

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    course = get_course(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE course SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('course.index'))
    return render_template('course/update.html', course=course)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_course(id)
    db = get_db()
    db.execute('DELETE FROM course WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('course.index'))