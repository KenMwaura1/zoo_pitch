from dataclasses import dataclass
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from commands import db, login


@login.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    secure_password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('UserPitch', backref='user', lazy='dynamic')

    # comment = db.relationship('Comment', backref='user', lazy='dynamic')
    # upvote = db.relationship('Upvote', backref='user', lazy='dynamic')
    # downvote = db.relationship('Downvote', backref='user', lazy='dynamic')

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def set_password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'


@dataclass
class UserPitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    pitch = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow())
    category = db.Column(db.String(255), index=True, nullable=False)

    # comment = db.relationship('Comment',backref='pitch',lazy='dynamic')
    # upvote = db.relationship('Upvote',backref='pitch',lazy='dynamic')
    # downvote = db.relationship('Downvote',backref='pitch',lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.post}'
