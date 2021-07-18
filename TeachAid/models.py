from datetime import datetime
from flask import current_app
from TeachAid import db, login
from TeachAid.coursesearch import add_to_index, remove_from_index, query_index
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

students = db.Table('students',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class Course(SearchableMixin, db.Model):
    __searchable__=['title']
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(140))
    outline = db.Column(db.String(240))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def avatar(self, size):
        digest = self.id
        return 'https://avatars.dicebear.com/api/jdenticon/{}.svg?w={}&h={}'.format(
            digest, size, size)

    def __repr__(self):
        return '<Course {}>'.format(self.title)

class Module(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    module_name = db.Column(db.String(140))
    course = db.relationship('Course', backref=db.backref('modules', lazy='dynamic', collection_class=list))

class YouTubeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(240))
    url=db.Column(db.String(140))
    channel_title=db.Column(db.String(140))
    channel_url=db.Column(db.String(140))
    image_url=db.Column(db.String(100))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    module = db.relationship('Module', backref=db.backref('youtube_content',lazy='dynamic', collection_class=list))
    
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

    def learn(self, course):
        if not self.is_learning(course):
            self.learns.append(course)

    def unfollow(self, course):
        if self.is_learning(course):
            self.learns.remove(course)

    def is_learning(self, course):
        return self.learns.filter(
            students.c.course_id == course.id).count() > 0

    def get_learning_courses(self):
        return Course.query.join(
            students, (students.c.course_id == Course.id)).filter(
                students.c.student_id == self.id)

    def get_own_courses(self):
        return Course.query.filter_by(lecturer_id=self.id)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
