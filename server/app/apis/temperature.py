from flask import Blueprint, jsonify
from app.models.mongo import Temperatures
from app.utils import auth, admin_only
from datetime import timedelta

api_temp = Blueprint('temperature', __name__)


@api_temp.route('/status')
@auth
@admin_only
def retrieve_last_temperature():
    try:
        return jsonify({
            'status': 'Data retrived',
            'data': Temperatures.get_last_measure().to_dict()
        }), 200
    except:
        return jsonify({'status': 'No data available'}), 500

@api_temp.route('/trend')
@auth
@admin_only
def retrieve_last_hour():
    # try:
        temps = Temperatures.get_time_range(timedelta(minutes=10))
        return jsonify({
            'status': 'Data retrived',
            'data': [temp.to_dict() for temp in temps]
        }), 200
    # except:
    #     return jsonify({'status': 'No data available'}), 500