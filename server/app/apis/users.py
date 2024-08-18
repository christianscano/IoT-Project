from flask import Blueprint, request, session, jsonify
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.models.sqlite import *
from app.utils import auth, admin_only
from .utils import validate_input

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
    
@api_user.route('/add_tag', methods=['POST'])
@auth
@admin_only
def add_new_tag():
    try:
        tag_id   = request.json['tag_id'].strip().upper()
        username = request.json['username'].strip()

        User.assign_tag(username, tag_id)
        
        return jsonify({"status": "Tag correctly assigned"}), 200
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    except Exception as e:
        return jsonify({"status": e.message}), 400


@api_user.route('/signin', methods=['POST'])
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

            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "Wrong credentials"}), 400
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    except VerifyMismatchError:
        return jsonify({"status": "Wrong credentials"}), 400
    
@api_user.route('/logout')
@auth
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)

    return jsonify({"status": "ok"}), 200

@api_user.route('/')
@auth
@admin_only
def retrive_list_users():
    users = User.get_all_users()
    return jsonify({
        "status": "ok",
        "data": [user.to_dict() for user in users]
    }), 200

@api_user.route('/', methods=['POST'])
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
            return jsonify({"status": "Invalid characters"}), 400

        User.create_user(username, name, surname, role, password)
                
        return jsonify({"status": "User created succesfully"}), 200
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    except UserExistException as e:
        return jsonify({"status": e.message}), 400
    except InvalidRoleException as e:
        return jsonify({"status": e.message}), 400 

@api_user.route('/<int:id>', methods=['DELETE'])
@auth
@admin_only
def delete_user():
    try:
        user = User.find_user_by_id(id)
        if not user:
            return jsonify({"status": "User not found"}), 400

        User.delete_user(id)

        return jsonify({"status": "User deleted succesfully"}), 200
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400
    
@api_user.route('/change_password', methods=['POST'])
@auth
def reset_password():
    try:
        old_password = request.json['old_password'].strip()
        new_password = request.json['new_password'].strip()

        if not validate_input(new_password):
            return jsonify({"status": "Invalid characters"}), 400

        try:
            User.reset_password(
                session['id'], 
                old_password, 
                new_password
            )
        except InvalidCredentialsException as e:
            return jsonify({"status": e.message}), 400
        except UserNotExistException as e:
            return jsonify({"status": e.message}), 400
        
        return jsonify({'status': 'Password changed successfully'}), 200
    except KeyError:
        return jsonify({"status": "Invalid parameters"}), 400