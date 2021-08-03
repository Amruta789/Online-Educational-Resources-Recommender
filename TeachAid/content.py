from flask import (
    Blueprint, flash, redirect, g, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from TeachAid.models import Course, Module, Content
from TeachAid.forms import CourseForm, EmptyForm, ModuleForm, SearchForm, ContentForm
from TeachAid import db
from flask_uploads import UploadSet, DEFAULTS, UploadNotAllowed

bp = Blueprint('content', __name__)
# DEFAULTS contains ('txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 
# 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml')
coursecontents = UploadSet('coursecontents', DEFAULTS+('pdf','jfif','odt'))

@bp.route('/<int:moduleid>/createcontent', methods=('POST',))
@login_required
def create(moduleid):
    form = ContentForm()
    module = Module.query.filter_by(id=moduleid).first()
    print(DEFAULTS)
    if form.validate_on_submit():
        content = Content(title=form.title.data)
        if form.description.data:
            content.description=form.description.data
        if form.url.data:
            content.url=form.url.data
        if form.file.data:
            fileuploaded=form.file.data
            try:
                filename = coursecontents.save(fileuploaded)
            except UploadNotAllowed:
                flash('The upload was not allowed.', category='warning')
            else:
                content.file_path='coursecontents/'+filename
        db.session.add(content)
        module.content.append(content)
        db.session.commit()
        flash('Your content is now live!')
        return redirect(url_for('course.get_course',id=module.course_id))

@bp.route('/<int:contentid>/updatecontent', methods=('GET','POST'))
@login_required
def update(contentid):
    form = ContentForm()
    content = Content.query.filter_by(id=contentid).first()
    module = Module.query.filter_by(id=content.module_id).first()
    course = Course.query.filter_by(id=module.course_id).first()
    if content is None:
          flash('Content not found.')
          return redirect(url_for('index'))
    if form.validate_on_submit():
        content.title = form.title.data
        if form.description.data:
            content.description = form.description.data
        if form.url.data:
            content.url = form.description.url
        if form.file.data:
            fileuploaded=form.file.data
            try:
                filename = coursecontents.save(fileuploaded, name=form.file.data.filename)
            except UploadNotAllowed:
                flash('The upload was not allowed.', category='warning')
            else:
                content.file_path='coursecontents/'+filename
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('course.get_course', id=module.course_id))
    elif request.method == 'GET':
        result={}
        result['title'] = content.title
        if content.description:
            result['description'] = content.description
        if content.url:
            result['url']= content.url 
    return jsonify(result)

@bp.route('/<int:id>/deletefile', methods=('POST',))
@login_required
def delete_file(id):
    content = Content.query.filter_by(id=id).first()
    if content.file_path:
        content.file_path=None
    db.session.commit()
    flash('This file has been deleted')
    return '', 200

@bp.route('/<int:id>/deletecontent', methods=('POST',))
@login_required
def delete_content(id):
    content = Content.query.filter_by(id=id).first()
    module = Module.query.filter_by(id=content.module_id).first()
    if not content.hidden:
        content.hidden=True
    db.session.commit()
    flash('This content has been deleted')
    return redirect(url_for('course.get_course',id=module.course_id))