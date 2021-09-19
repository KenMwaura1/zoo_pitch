from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main
from ..models import UserPitch
from .forms import NewPitchForm
from app.commands import db


@main.route('/')
def index():
    """
    function to display index template
    :return: index.html
    """
    session = db.Session()
    a = session.query(UserPitch).order_by(UserPitch.time)
    all_pitches = UserPitch.query.order_by(UserPitch.time)
    startup_pitches = session.query(UserPitch).filter_by(category='startup').order_by(UserPitch.time)

    return render_template('index.html', startup_pitches=startup_pitches, pitches=a)


@main.route('/New-Pitch', methods=['POST', 'GET'])
@login_required
def new_pitch():
    form = NewPitchForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        new_pitch_object = NewPitchForm(post=post, user_id=user_id, category=category,
                                        title=title)
        new_pitch_object.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('create_pitch.html', form=form)
