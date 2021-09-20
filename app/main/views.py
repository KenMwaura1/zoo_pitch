from flask import render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user

from . import main
from ..models import User, UserPitch, Comment, Downvotes, Upvote
from .forms import NewPitchForm, NewCommentForm, ProfileUpdate
from app.commands import db, photos


@main.route('/')
def index():
    """
    function to display index template
    :return: index.html
    """
    all_pitches = db.session.query(UserPitch).order_by(db.desc(UserPitch.time))
   # all_pitches = UserPitch.query.order_by(UserPitch.time)
    startup_pitches = db.session.query(UserPitch).filter_by(category='Startup').order_by(db.desc(UserPitch.time))
    idea_pitches = db.session.query(UserPitch).filter_by(category='Idea').order_by(db.desc(UserPitch.time))
    funding_pitches = db.session.query(UserPitch).filter_by(category='Funding').order_by(db.desc(UserPitch.time))
    event_pitches = db.session.query(UserPitch).filter_by(category='Event').order_by(db.desc(UserPitch.time))
    return render_template('index.html', startup_pitches=startup_pitches, all_pitches=all_pitches,
                           idea_pitches=idea_pitches, funding_pitches=funding_pitches, event_pitches=event_pitches)


@main.route('/New-Pitch', methods=['POST', 'GET'])
@login_required
def new_pitch():
    form = NewPitchForm()
    if form.validate_on_submit():
        pitch_title = form.pitch_title.data
        pitch = form.pitch.data
        pitch_category = form.pitch_category.data
        user_id = current_user._get_current_object().id
        new_pitch_object = UserPitch(pitch=pitch, user_id=user_id, category=pitch_category,
                                     title=pitch_title)
        new_pitch_object.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('create_pitch.html', form=form)


@main.route('/user/<string:name>')
def profile(name):
    user = db.session.query(User).filter_by(username=name).first()
    user_id = current_user._get_current_object().id
    pitches = db.session.query(UserPitch).filter(user_id == user_id).all()
    if user is None:
        abort(404)

    return render_template("user_profile/profile.html", user=user, pitches=pitches)


@main.route('/user/<name>/update_profile', methods=['POST', 'GET'])
@login_required
def update_profile(name):
    form = ProfileUpdate()
    user = db.session.query(User).filter_by(username=name).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for('.profile', name=name))
    return render_template('user_profile/update.html', form=form)


@main.route('/user/<name>/update/pic', methods=['POST'])
@login_required
def update_pic(name):
    user = db.session.query(User).filter_by(username=name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', name=name))


@main.route('/comment/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def comment(pitch_id):
    form = NewCommentForm()
    pitch = db.session.query(UserPitch).get(pitch_id)
    all_comments = db.session.query(Comment).filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment, user_id=user_id, pitch_id=pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id=pitch_id))
    return render_template('comment.html', form=form, pitch=pitch, all_comments=all_comments)


@main.route('/like/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def like(pitch_id):
    get_pitches = Upvote.get_upvotes(pitch_id)
    valid_string = f'{current_user.id}:{pitch_id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string + " " + to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index', id=pitch_id))
        else:
            continue
    new_vote = Upvote(user=current_user, pitch_id=pitch_id)
    new_vote.save()
    return redirect(url_for('main.index', pitch_id=pitch_id))


@main.route('/dislike/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def dislike(pitch_id):
    pitch = Downvotes.get_downvotes(pitch_id)
    valid_string = f'{current_user.id}:{pitch_id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string + " " + to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index', id=pitch_id))
        else:
            continue
    new_downvote = Downvotes(user=current_user, pitch_id=pitch_id)
    new_downvote.save()
    return redirect(url_for('main.index', pitch_id=pitch_id))
