from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import IMAGES, UploadSet, configure_uploads

mail = Mail()
login = LoginManager()
db = SQLAlchemy()
login.session_protection = 'strong'
login.login_view = ''
photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    """
    app factory function
    :param config_name:
    :return: app
    """
    app = Flask(__name__)
