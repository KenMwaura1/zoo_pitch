from dataclasses import dataclass
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.commands import db, login


@login.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    secure_password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('UserPitch', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    upvote = db.relationship('Upvote', backref='user', lazy='dynamic')
    downvotes = db.relationship('Downvotes', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("You cannot read password attribute")

    @password.setter
    def password(self, password):
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
    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')
    upvote = db.relationship('Upvote', backref='pitch', lazy='dynamic')
    downvotes = db.relationship('Downvotes', backref='pitch', lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def delete_pitch(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.post}'


@dataclass
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        return Comment.query.filter_by(pitch_id=pitch_id).all()

    def __repr__(self):
        return f'comment:{self.comment}'


@dataclass
class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, id):
        return Upvote.query.filter_by(pitch_id=id).all()

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'


@dataclass
class Downvotes(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        return Downvotes.query.filter_by(pitch_id=id).all()

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
