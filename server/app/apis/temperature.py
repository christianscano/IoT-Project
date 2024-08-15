from flask import Blueprint, request, session, jsonify
from app.models.mongo import Temperatures
from .utils import auth, admin_only
from datetime import timedelta

api_temp = Blueprint('temperature', __name__)


@api_temp.route('/status')
@auth
@admin_only
def retrieve_last_temperature():
    return jsonify(
        Temperatures.get_last_measure().to_dict()
    ), 200

@api_temp.route('/last_hour')
@auth
@admin_only
def retrieve_last_hour():
    temps = Temperatures.get_time_range(timedelta(hours=1))
    return jsonify({
        'values': [temp.to_dict() for temp in temps]
    }), 200