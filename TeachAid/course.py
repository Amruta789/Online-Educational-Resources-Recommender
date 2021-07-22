# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 16:38:30 2021

@author: Amruta
"""
from flask import (
    Blueprint, flash, redirect, g, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from TeachAid.models import Course, Module
from TeachAid.forms import CourseForm, EmptyForm, ModuleForm, SearchForm
from TeachAid import db

bp = Blueprint('course', __name__)

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()

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

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    courses, total = Course.search(g.search_form.q.data, page,current_app.config['COURSES_PER_PAGE'])
    next_url = url_for('course.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['COURSES_PER_PAGE'] else None
    prev_url = url_for('course.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('course/search.html', title='Search', courses=courses,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CourseForm()
    template_form = ModuleForm(prefix='modules-_-')
    if form.validate_on_submit():
        course = Course(title=form.title.data, outline=form.outline.data, lecturer=current_user)
        for module in form.modules.data:
            new_module = Module(**module)
            course.modules.append(new_module)
        db.session.add(course)
        db.session.commit()
        flash('Your course is now live!')
        return redirect(url_for('index'))
    return render_template('course/create.html', form=form, _template=template_form)

@bp.route('/<int:id>/course', methods=('GET', 'POST'))
@login_required
def get_course(id):
    form=EmptyForm()
    course = Course.query.filter_by(id=id).first()
    if course is None:
          flash('Course not found.')
          return redirect(url_for('index'))    
    return render_template('course/course.html', course=course, form=form)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = CourseForm()
    template_form = ModuleForm(prefix='modules-_-')
    course = Course.query.filter_by(id=id).first()
    if course is None:
          flash('Course not found.')
          return redirect(url_for('index'))
    if form.validate_on_submit():
        course.title = form.title.data
        course.outline = form.outline.data
        for moduleform in form.modules.data:
            flag=0 
            for modulecourse in course.modules:        
                if(moduleform['module_name'] == modulecourse.module_name):
                    flag=1
            if flag==0:
                new_module = Module(**moduleform)  
                course.modules.append(new_module)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('course.get_course', id=id))
    elif request.method == 'GET':
        form.title.data = course.title
        form.outline.data = course.outline
        for module in course.modules:
            form.modules.append_entry(module)
    return render_template('course/update.html', course=course, form=form, _template=template_form)

#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
#def delete(id):
#   get_course(id)
#    db = get_db()
#    db.execute('DELETE FROM course WHERE id = ?', (id,))
#    db.commit()
#    return redirect(url_for('course.index'))