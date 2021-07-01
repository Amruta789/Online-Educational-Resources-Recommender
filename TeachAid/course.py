# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 16:38:30 2021

@author: Amruta
"""
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from TeachAid.models import Course
from TeachAid.forms import CourseForm
from TeachAid import db

bp = Blueprint('course', __name__)

@bp.route('/')
def index():
    courses = Course.query.all()
    return render_template('course/index.html', courses=courses)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data, outline=form.outline.data, lecturer=current_user)
        db.session.add(course)
        db.session.commit()
        flash('Your course is now live!')
        return redirect(url_for('index'))
    return render_template('course/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = CourseForm()
    course = Course.query.filter_by(id==id).first()
    if course is None:
          flash('Course not found.')
          return redirect(url_for('index'))
    if form.validate_on_submit():
        course.title = form.title.data
        course.outline = form.outline.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('course.update'))
    elif request.method == 'GET':
        form.title.data = course.title
        form.outline.data = course.outline
    return render_template('course/update.html', form=form)

#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
#def delete(id):
#   get_course(id)
#    db = get_db()
#    db.execute('DELETE FROM course WHERE id = ?', (id,))
#    db.commit()
#    return redirect(url_for('course.index'))