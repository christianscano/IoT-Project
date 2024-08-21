from flask import Blueprint, render_template, session
from app.models.sqlite import User
from app.utils import auth, admin_only, security_only, code_to_user_role

front = Blueprint(
    'frontend', 
    __name__, 
    static_folder='static', 
    template_folder='templates',
)

def translate(role):
    if role == 'admin':
        return 'System Manager'
    elif role == 'security':
        return 'Security Staff'
    else:
        return 'System Administrator'

@front.route('/')
@front.route('/login')
def index():
    return render_template('login.html')

@front.route('/home')
@auth
def home():
    return render_template(
        'home.html', 
        role=code_to_user_role(session['role'])
    )

@front.route('/dashboard')
@auth
def dashboard():
    user = User.find_user_by_id(session['id']).to_dict()
    user['role'] = translate(user['role'])

    if user['tag_id'] is None:
        user['tag_id'] = 'Not assigned'

    return render_template('dashboard.html', user=user)

@front.route('/temperature')
@auth
@admin_only
def temperature():
    return render_template('temperature.html')

@front.route('/intrusion')
@auth
@security_only
def intrusion():
    return render_template('intrusion.html')

@front.route('/logs')
@auth
def logs():
    return render_template(
        'logs.html',
        role=code_to_user_role(session['role'])
    )

@front.route('/users')
@auth
@admin_only
def users():
    return render_template('users.html')

@front.route('/change_password')
@auth
def change_password():
    return render_template('change_password.html')

@front.route('/accesses')
@auth
@admin_only
def accesses():
    return render_template('accesses.html')