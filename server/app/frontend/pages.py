from flask import Blueprint, render_template

front = Blueprint('frontend', __name__)

@front.route('/')
def index():
    return render_template('login.html')