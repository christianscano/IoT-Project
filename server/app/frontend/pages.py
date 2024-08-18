from flask import Blueprint, render_template, session
from app.models.sqlite import User
from app.utils import auth, admin_only, security_only


front = Blueprint(
    'frontend', 
    __name__, 
    static_folder='static', 
    template_folder='templates',
)

@front.route('/')
@front.route('/login')
def index():
    return render_template('login.html')

@front.route('/home')
@auth
def home():
    return render_template('home.html')

@front.route('/dashboard')
@auth
def dashboard():
    user = User.find_user_by_id(session['id']).to_dict()
    return render_template('dashboard.html', user=user)

@front.route('/temperature')
@auth
@admin_only
def temperature():
    return render_template('temperature.html', data={})

@front.route('/intrusion')
@auth
@security_only
def intrusion():
    return render_template('intrusion.html', data={})

@front.route('/logs')
@auth
def logs():
    return render_template('logs.html', data={})

@front.route('/users')
@auth
@admin_only
def users():
    return render_template('users.html', data={})
