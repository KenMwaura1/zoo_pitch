from flask import render_template
from . import main


@main.app_errorhandler(404)
def error_handler(error):
    """
    function to render 404 page
    :param error:
    :return: 404 error page
    """
    return render_template('404.html'), 404
