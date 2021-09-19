from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, Required
from app.models import User


class UserRegForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(), Email()])
    username = StringField('Enter Your Username', validators=[Required()])
    password = PasswordField('Password',
                             validators=[Required(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords', validators=[Required()])
    submit = SubmitField('Sign Up')

    @classmethod
    def validate_email(cls, data_field):
        if cls.query.filter_by(email=data_field.data).first():
            raise ValidationError("The Email has already been taken!")

    @classmethod
    def validate_username(cls, data_field):
        if cls.query.filter_by(username=data_field.data).first():
            raise ValidationError("The username has already been taken")

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Login')


