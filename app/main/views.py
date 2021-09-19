from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main
from ..models import User


@main.route('/')
def index():
    """
    function to display index template
    :return: index.html
    """
    return render_template('index.html')