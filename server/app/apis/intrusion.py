from flask import Blueprint, jsonify
from app.utils import auth, security_only
from app.models.mongo import IntrusionSystem
from app.mqtt import mqtt_handler

api_intrusion = Blueprint('intrusion', __name__)


@api_intrusion.route('/status')
@auth
@security_only
def retrieve_system_status():
    try:
        return jsonify({
            'status': 'Information retrieved.',
            'enabled': IntrusionSystem.get_last_status()
        }), 200
    except:
        return jsonify({"stauts": "Status not available."}), 500

@api_intrusion.route('/enable')
@auth
@security_only
def enable_detection_system():
    try:
        if not IntrusionSystem.get_last_status():
            IntrusionSystem.update_status(True)
            mqtt_handler.enable_intrusion_system()

        return jsonify({"status": "System activated correctly."}), 200
    except:
        return jsonify({"status": "Error activacting the system."}) , 500

@api_intrusion.route('/disable')
@auth
@security_only
def disable_detection_system():
    try:
        IntrusionSystem.update_status(False)
        mqtt_handler.disable_intrusion_system()

        if IntrusionSystem.get_last_alarm_status():
            IntrusionSystem.add_alarm_log(False)
            mqtt_handler.disable_alarm()

        return jsonify({"status": "System deactivated correctly."}), 200
    except:
        return jsonify({"status": "Error deactivating the system."}) , 500

@api_intrusion.route('/status_alarm')
@auth
@security_only
def retrieve_alarm_status():
    try:
        status = IntrusionSystem.get_last_alarm_status()
        if status is None:
            return jsonify({
                'enabled': False,
                "status": "Status retrieved correctly."
            }), 200
        else:
            return jsonify({
                'enabled': status.to_dict()['enabled'],
                "status": "Status retrieved correctly."
            }), 200
    except:
        return jsonify({"status": "Error retriving alarm status."}), 500
        
@api_intrusion.route('/disable_alarm')
@auth
@security_only
def disable_alarm():
    try:
        if IntrusionSystem.get_last_status():
            IntrusionSystem.add_alarm_log(False)
            mqtt_handler.disable_alarm()
        return jsonify({"status": "Alarm deactivated correctly."}), 200
    except:
        return jsonify({"status": "Error deactivating the alarm."}), 500