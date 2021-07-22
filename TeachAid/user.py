from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from TeachAid.models import User, Course
from TeachAid.forms import LoginForm, RegistrationForm, EmptyForm, EditProfileForm
from TeachAid import db

bp = Blueprint('user', __name__,  url_prefix='/user')

@bp.route('/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    courses = Course.query.all()
    return render_template('user/user.html', user=user, courses=courses, form=form)

@bp.route('/<username>/profile')
@login_required
def userprofile(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    courses = Course.query.all()
    return render_template('user/public_profile.html', user=user, courses=courses, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route('/learn/<courseid>', methods=['POST'])
@login_required
def learn(courseid):
    form = EmptyForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(id=courseid).first()
        if course is None:
            flash('Course not found.')
        current_user.learn(course)
        db.session.commit()
        flash('You are learning {}!'.format(course.title))
        return redirect(url_for('index'))


@bp.route('/unfollow/<courseid>', methods=['POST'])
@login_required
def unfollow(courseid):
    form = EmptyForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(id=courseid).first()
        if user is None:
            flash('Course not found.')
            return redirect(url_for('index'))
        current_user.unfollow(course)
        db.session.commit()
        flash('You are not following {}.'.format(course.title))
        return redirect(url_for('index'))