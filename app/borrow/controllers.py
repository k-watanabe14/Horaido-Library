from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth.controllers import login_required
from app import db
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_borrow = Blueprint('borrow', __name__, url_prefix='/borrow')


@mod_borrow.route('/')
@login_required
def index():
    return render_template('borrow/index.html')