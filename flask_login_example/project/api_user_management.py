from flask import Blueprint, render_template, redirect, url_for, redirect, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .data_models import User
from . import db

api_user_management = Blueprint('api_user_management', __name__)


@api_user_management.route('/newaccount')
def newaccount():
    return render_template('newaccount.html')

@api_user_management.route('/newaccount', methods=['POST'])
def newaccountPost():
    
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        flash('The user already exists')
        return redirect(url_for('api_user_management.newaccount'))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('api_user_management.login'))

@api_user_management.route('/login')
def login():
    return render_template('login.html')

@api_user_management.route('/login', methods=['POST'])
def loginPost():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your username and password and try again.')
        return redirect(url_for('api_user_management.login'))
    
    login_user(user, remember=remember)
    
    return redirect(url_for('api_platform.userspace'))


@api_user_management.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('api_platform.index'))
