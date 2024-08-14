from flask import Blueprint
from .user import api_user
from .logs import api_logs
from .temperature import api_temp
from .intrusion import api_intrusion

api = Blueprint('api', __name__)

api.register_blueprint(api_user, url_prefix='/user')
api.register_blueprint(api_logs, url_prefix='/logs')
api.register_blueprint(api_temp, url_prefix='/temperature')
api.register_blueprint(api_intrusion, url_prefix='/intrusion')
