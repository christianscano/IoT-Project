from flask import Blueprint, request, session, jsonify
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.models.sqlite import *
from .utils import auth, admin_only, validate_input

api_user = Blueprint('user', __name__)


@api_user.route('/access_rfid')
def rfid_auth():
    try:
        user = User.find_by_tagid(request.args.get('uid'))
        if not user:
            return '', 403
        
        AccessLog.add_log(user.id, user.tag_id)
        
        return '', 200
    except:
        return '', 500

@api_user.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username'].strip()
        password = request.json['password'].strip()

        user = User.find_user(username)
        ph   = PasswordHasher()

        if user:
            ph.verify(user.password, password)

            session['id']       = user.id
            session['username'] = user.username
            session['role']     = user.role

            return '', 201
        else:
            return jsonify({"status": "Wrong credentials"}), 401
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    except VerifyMismatchError:
        return jsonify({"status": "Wrong credentials"}), 401
    
@api_user.route('/logout')
@auth
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)

    return '', 200

@api_user.route('/add', methods=['POST'])
@auth
@admin_only
def add_new_user():
    try:
        username = request.json['username'].strip()
        name     = request.json['name'].strip()
        surname  = request.json['surname'].strip()
        password = request.json['password'].strip()
        role     = request.json['role'].strip()

        if not validate_input(username) or \
            not validate_input(name) or \
            not validate_input(surname) or \
            not validate_input(password):
            return jsonify({"status": "Invalid characters"}), 401

        User.create_user(username, name, surname, role, password)
                
        return '', 201
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    except UserExistException as e:
        return jsonify({"status", e.message}), 401
    except InvalidRoleException as e:
        return jsonify({"status", e.message}), 401 

@api_user.route('/delete', methods=['POST'])
@auth
@admin_only
def delete_user():
    try:
        username = request.json['username'].strip()

        user = User.find_user(username)
        if not user:
            return jsonify({"status": "User not found"}), 401

        user.delete_user()

        return '', 201
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400

@api_user.route('/add_tag', methods=['POST'])
@auth
@admin_only
def add_new_tag():
    try:
        tag_id   = request.json['tag_id'].strip().upper()
        username = request.json['username'].strip()

        User.assign_tag(username, tag_id)
        
        return '', 201
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    except Exception as e:
        return jsonify({"status": e.message}), 401

@api_user.route('/reset_password', methods=['POST'])
@auth
def reset_password():
    try:
        new_password = request.json['new_password'].strip()

        if not validate_input(new_password):
            return jsonify({"status": "Invalid characters"}), 401
 
        User.reset_password(session['username'], new_password)

        return '', 201
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    
@api_user.route('/all')
@auth
@admin_only
def retrive_list_users():
    users = User.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200