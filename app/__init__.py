from flask import Flask


def create_app(config_name):
    """
    app factory function
    :param config_name:
    :return: app
    """
    app = Flask(__name__)
    from .main import main as main_bp

    app.register_blueprint(main_bp)

    return app
