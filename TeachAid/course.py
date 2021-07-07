# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 16:38:30 2021

@author: Amruta
"""
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from TeachAid.models import Course
from TeachAid.forms import CourseForm, EmptyForm
from TeachAid import db

bp = Blueprint('course', __name__)

@bp.route('/')
def index():
    form=EmptyForm()
    page = request.args.get('page', 1, type=int)
    courses = Course.query.order_by(Course.created.desc()).paginate(
        page, current_app.config['COURSES_PER_PAGE'], False)
    next_url = url_for('index', page=courses.next_num) \
        if courses.has_next else None
    prev_url = url_for('index', page=courses.prev_num) \
        if courses.has_prev else None
    return render_template('course/index.html', courses=courses.items, form=form, next_url=next_url, prev_url=prev_url)

@bp.route('/searchweb')
def search_web():
    return render_template('course/search.html')

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
    return render_template('course/create.html', form=form)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = CourseForm()
    course = Course.query.filter_by(id=id).first()
    if course is None:
          flash('Course not found.')
          return redirect(url_for('index'))
    if form.validate_on_submit():
        course.title = form.title.data
        course.outline = form.outline.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('course.update', id=id))
    elif request.method == 'GET':
        form.title.data = course.title
        form.outline.data = course.outline
    return render_template('course/update.html', course=course, form=form)

#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
#def delete(id):
#   get_course(id)
#    db = get_db()
#    db.execute('DELETE FROM course WHERE id = ?', (id,))
#    db.commit()
#    return redirect(url_for('course.index'))