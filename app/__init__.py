from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_name):
    """
    app factory function
    :param config_name:
    :return: app
    """
    app = Flask(__name__)
    from .main import main as main_bp
    from auth import auth
    # initialize bootstrap
    bootstrap.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
