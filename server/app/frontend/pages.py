from flask import Blueprint, render_template

front = Blueprint(
    'frontend', 
    __name__, 
    static_folder='static', 
    template_folder='templates',
)

@front.route('/')
def index():
    return render_template('login.html')

@front.route('/home')
def home():
    return render_template('home.html')

@front.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')