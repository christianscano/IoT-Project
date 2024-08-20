from flask import Blueprint, request, session, jsonify
from app.models.sqlite import *
from app.utils import code_to_user_role
from app.utils import auth, admin_only

api_logs = Blueprint('logs', __name__)


@api_logs.route('/', methods=['GET'])
@auth
def filter_logs():
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')
    username   = request.args.get('username')
    is_admin   = code_to_user_role(session.get('role')) == 'admin'

    try:
        filter_params = dict()

        # Username filter
        if username and is_admin:
            filter_params['username'] = username
        elif not is_admin:
            filter_params['username'] = session.get('username')
        
        # Date filters
        if start_date:
            filter_params['start_date'] = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            filter_params['end_date'] = datetime.strptime(end_date, '%Y-%m-%d')

        if is_admin and not filter_params:
            logs = AccessLog.retrieve_with_filters()
        elif 'username' in filter_params or filter_params:
            logs = AccessLog.retrieve_with_filters(**filter_params)
        else:
            logs = AccessLog.retrieve_with_filters(session.get('username'))

        return jsonify({"data": logs, 'status': 'Data retrieved'}), 200

    except UserNotExistException as e:
        return jsonify({"status": e.message}), 400
    except ValueError as e:
        return jsonify({'status': e.message}), 400
    except:
        return jsonify({'status': 'Something went wrong'}), 500