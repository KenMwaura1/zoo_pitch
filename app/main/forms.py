from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class NewPitchForm(FlaskForm):
    """
    class to create form to enable user to create new forms
    """
    pitch_title = StringField('Pitch Title', validators=[Required()])
    pitch_category = SelectField('Pitch Category', choices=[('Startup', 'Startup'), ('Idea', 'Idea'),
                                                            ('Funding', 'Funding'), ('Event', 'Event')],
                                 validators=[Required()])
    pitch = TextAreaField('Type your pitch', validators=[Required()])
    submit = SubmitField('Submit')


class NewCommentForm(FlaskForm):
    comment = TextAreaField('Tell us your thoughts', validators=[Required()])
    submit = SubmitField('Submit Comment')


class ProfileUpdate(FlaskForm):
    bio = TextAreaField('Tell us something about yourself', validators=[Required()])
    submit = SubmitField('Submit Profile')
