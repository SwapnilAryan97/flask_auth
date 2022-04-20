from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from app.db import db
from app.db.models import User
from app.auth.decorators import admin_required
from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = register_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()
            flash('Congratulations, you are now a registered user!', "success")
            return redirect(url_for('auth.login'), 302)
        else:
            flash('Already Registered')
            return redirect(url_for('auth.login'), 302)
    return render_template('register.html', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome", 'success')
            return redirect(url_for('auth.dashboard'))
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@auth.route('/profile', methods=['POST', 'GET'])
def edit_profile():
    user = User.query.get(current_user.get_id())
    form = profile_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Profile', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('profile_edit.html', form=form)


@auth.route('/account', methods=['POST', 'GET'])
def edit_account():
    user = User.query.get(current_user.get_id())
    form = security_form(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Password or Email', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('manage_account.html', form=form)
