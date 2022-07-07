from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user

api_platform = Blueprint('api_platform', __name__)

@api_platform.route('/userspace')
@login_required
def userspace():
    return render_template('userspace.html', user_name=current_user.name)

@api_platform.route('/')
def index():
    return render_template('front.html')