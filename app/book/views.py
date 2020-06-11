from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth.views import login_required
from app import db
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_return = Blueprint('return', __name__, url_prefix='/return')


@mod_return.route('/')
@login_required
def index():
    return render_template('return/index.html')