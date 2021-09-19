from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


mail = Mail()
login = LoginManager()

login.session_protection = 'strong'
login.login_view = 'auth.login'


photos = UploadSet('photos', IMAGES)
db = SQLAlchemy()


def photo_config(app):
    configure_uploads(app, photos)


def login_config(app):
    login.init_app(app)


def mail_config(app):
    mail.init_app(app)


def db_config(app):
    db.init_app(app)
