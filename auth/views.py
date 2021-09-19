from flask import flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from .forms import UserLoginForm, UserRegForm
from app.commands import db
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')
    return render_template('auth/login.html', loginform=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route('/signup', methods = ["GET","POST"])
def signup():
    form = UserRegForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        user.save_user()
        mail_message("Welcome to Pitch-World","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', r_form = form)