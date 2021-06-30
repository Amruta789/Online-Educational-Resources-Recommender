from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from TeachAid.models import User, Course
from TeachAid.forms import LoginForm, RegistrationForm

bp = Blueprint('user', __name__)

@bp.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    courses = [
        {'lecturer': user, 'title': 'Test course #1'},
        {'lecturer': user, 'title': 'Test course #2'}
    ]
    return render_template('user/user.html', user=user, courses=courses)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
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