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
from TeachAid.forms import CourseForm, EmptyForm, ModuleForm, SearchForm, ContentForm
from TeachAid import db
from flask_uploads import UploadSet, IMAGES, UploadNotAllowed

bp = Blueprint('course', __name__)

courseprofiles = UploadSet('courseprofiles', IMAGES+('jfif','tif','tiff'))

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
    form=EmptyForm()
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    courses, total = Course.search(g.search_form.q.data, page,current_app.config['COURSES_PER_PAGE'])
    next_url = url_for('course.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['COURSES_PER_PAGE'] else None
    prev_url = url_for('course.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('course/search.html', title='Search', courses=courses, form=form,
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
        if form.profile.data:
            profileimage = form.profile.data
            try:
                filename = courseprofiles.save(profileimage, name='course_'+str(course.id)+'_'+form.profile.data.filename)
            except UploadNotAllowed:
                flash('The upload was not allowed.', category='warning')
            else:
                course.profileimg='courseprofiles/'+filename
        db.session.add(course)
        db.session.commit()
        flash('Your course is now live!')
        return redirect(url_for('index'))
    return render_template('course/create.html', form=form, _template=template_form)

@bp.route('/<int:id>/course', methods=('GET', 'POST'))
@login_required
def get_course(id):
    form=EmptyForm()
    content_form=ContentForm()
    course = Course.query.filter_by(id=id).first()
    if course is None:
          flash('Course not found.')
          return redirect(url_for('index'))    
    return render_template('course/course.html', course=course, form=form, content_form=content_form)

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
        if form.profile.data:
            profileimage = form.profile.data
            try:
                filename = courseprofiles.save(profileimage, name='course_'+str(current_user.id)+'_'+form.profile.data.filename)
            except UploadNotAllowed:
                flash('The upload was not allowed.', category='warning')
            else:
                course.profileimg='courseprofiles/'+filename
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('course.get_course', id=id))
    elif request.method == 'GET':
        form.title.data = course.title
        form.outline.data = course.outline
        for module in course.modules:
            form.modules.append_entry(module)
    return render_template('course/update.html', course=course, form=form, _template=template_form)

@bp.route('/<int:id>/togglecourse', methods=('POST',))
@login_required
def showhide(id):
    course = Course.query.filter_by(id=id).first()
    if not course.hidden:
        course.hidden=True
        db.session.commit()
        flash('This course is hidden from public')
    else:
        course.hidden=False
        db.session.commit()
        flash('This course is live again')
    return redirect(url_for('index'))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    course = Course.query.filter_by(id=id).first()
    db.session.delete(course)
    db.session.commit()
    flash('This course has been deleted')
    return redirect(url_for('index'))