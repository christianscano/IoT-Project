from flask import Blueprint, request, session, jsonify
from app.models.sqlite import *
from app.utils import code_to_user_role
from app.utils import auth, admin_only

api_logs = Blueprint('logs', __name__)


@api_logs.route('/all', methods=['GET'])
@auth
@admin_only
def get_all_logs():
    return jsonify(AccessLog.retrieve_all()), 200

@api_logs.route('/filters', methods=['GET'])
@auth
def filter_logs():
    date_begin = request.args.get('date_begin')
    date_end   = request.args.get('date_end')
    username   = request.args.get('username')

    try:
        # Filtering by date range
        if date_begin and date_end:
            if username:
                if code_to_user_role(session.get('role')) != 'admin':
                    logs = AccessLog.retrieve_by_date(
                        date_begin, 
                        date_end, 
                        session.get('username')
                    )
                else:
                    logs = AccessLog.retrieve_by_date(
                        date_begin, 
                        date_end, 
                        username
                    )
            else:
                logs = AccessLog.retrieve_by_date(date_begin, date_end)
        
        # Filtering by username
        if username:
            if code_to_user_role(session.get('role')) != 'admin':
                logs = AccessLog.retrieve_by_user(session.get('username'))
            else:
                logs = AccessLog.retrieve_by_user(username)

        return jsonify(logs), 200
    except UserNotExistException:
        return jsonify(list()), 200
    except:
        return jsonify({'status': 'Invalid parameters'}), 400