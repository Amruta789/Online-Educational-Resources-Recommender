from datetime import datetime
from flask import current_app
from TeachAid import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course', backref='lecturer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(140))
    outline = db.Column(db.String(240))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Course {}>'.format(self.body)