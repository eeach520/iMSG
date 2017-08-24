from . import auth
from .. import db
from werkzeug.security import check_password_hash
from flask import render_template, redirect, request, url_for, flash
from .forms import LoginForm
from ..models import User
from flask_login import login_required, logout_user, login_user, current_user


# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print(form.username.data)
        print(form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        print(user.username)
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index', name=current_user.username))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))
