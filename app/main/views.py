from flask import Blueprint, render_template, redirect
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_rq import get_queue

from app.models import EditableHTML

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(
        'calls/calls-list')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)


@main.route('/calls-list')
@login_required
def list_calls():
    return redirect(
        'calls/calls-list')

# TODO: Rest API
@main.route('/create-call')
@login_required
def create_call():
    return redirect(
        'calls/create-call')
