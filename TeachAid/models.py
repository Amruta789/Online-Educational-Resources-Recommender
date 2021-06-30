from datetime import datetime
from flask import current_app
from TeachAid import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

students = db.Table('students',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(140))
    outline = db.Column(db.String(240))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def avatar(self, size):
        digest = md5(self.id.encode('utf-8')).hexdigest()
        return 'https://avatars.dicebear.com/api/jdenticon/{}.svg?w={}&h={}'.format(
            digest, size, size)

    def __repr__(self):
        return '<Course {}>'.format(self.title)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course', backref='lecturer', lazy='dynamic')
    learns = db.relationship(
        'Course', secondary=students,
        primaryjoin=(students.c.student_id == id),
        secondaryjoin=(students.c.course_id == Course.id),
        backref=db.backref('students', lazy='dynamic'), lazy='dynamic')

    def learn(self, user):
        if not self.is_learning(user):
            self.students.append(user)

    def unfollow(self, user):
        if self.is_learning(user):
            self.students.remove(user)

    def is_learning(self, user):
        return self.students.filter(
            student.c.student_id == user.id).count() > 0

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
