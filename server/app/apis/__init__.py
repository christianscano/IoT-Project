from flask import Blueprint
from .user import api_user
from .logs import api_logs

api = Blueprint('api', __name__)

api.register_blueprint(api_user, url_prefix='/user')
api.register_blueprint(api_logs, url_prefix='/logs')