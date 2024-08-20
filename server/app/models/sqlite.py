from app.db import sqlite_db as db
from app.utils import user_role_to_code, code_to_user_role
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime

# ------------------
# Custom exceptions
# ------------------
class InvalidRoleException(Exception):
    def __init__(self):
        self.message = 'Invalid role.'
        super().__init__(self.message)

class UserNotExistException(Exception):
    def __init__(self):
        self.message = 'User does not exist.'
        super().__init__(self.message)

class UserExistException(Exception):
    def __init__(self):
        self.message = 'User already exists.'
        super().__init__(self.message)

class TagExistException(Exception):
    def __init__(self):
        self.message = 'Tag already assigned.'
        super().__init__(self.message)

class UserNotAllowedException(Exception):
    def __init__(self):
        self.message = 'Operation not allowed for this user.'
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = 'The old password is incorrect.'
        super().__init__(self.message)

class ValueError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# ----------------
# Database models
# ----------------
class User(db.Model):
    """
    A class to represent a User in the SQLite database. The kind attribute can assume 
    the following values:
        0 - System Manager
        1 - Security Staff
        2 - System Administrator
    """
    __tablename__ = 'Users'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name     = db.Column(db.String(30), nullable=False)
    surname  = db.Column(db.String(30), nullable=False)
    role     = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    tag_id   = db.Column(db.String(10), unique=True)
    # One-to-many relationship with Logs
    logs     = db.relationship('AccessLog', backref='user', lazy=True, cascade='all')

    def __init__(self, username, name, surname, role, password):
        self.username = username
        self.name     = name
        self.surname  = surname
        self.role     = role
        self.password = password
        self.tag_id   = None

    @classmethod
    def create_user(cls, username, name, surname, role, password):
        role = user_role_to_code(role)
        if role == -1:
            raise InvalidRoleException()
        
        if cls.query.filter_by(username=username).first():
            return UserExistException()
        
        ph = PasswordHasher()

        user = cls(username, name, surname, role, ph.hash(password))
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def find_user(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    @classmethod
    def reset_password(cls, id, old_password, new_password):
        user = cls.query.filter_by(id=id).first()

        if user is None:
            raise UserNotExistException()
        
        try:
            ph = PasswordHasher()
            ph.verify(user.password, old_password)

            user.password = ph.hash(new_password)
            
            db.session.commit()
        except VerifyMismatchError:
            raise InvalidCredentialsException()
    
    @classmethod
    def delete_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
    
    @classmethod
    def find_by_tagid(cls, uid):
        return cls.query.filter_by(tag_id=uid).first()
    
    @classmethod
    def assign_tag(cls, username, tag_id):
        user = cls.query.filter_by(username=username).first()
        if user is None:    
            raise UserNotExistException()
        
        if code_to_user_role(user.role) == 'admin':
            raise UserNotAllowedException()

        if cls.query.filter_by(tag_id=tag_id).first() is not None:
            raise TagExistException()
        
        user.tag_id = tag_id
        db.session.commit()

    @classmethod
    def remove_tag(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user is None:
            raise UserNotExistException()
        
        user.tag_id = None
        db.session.commit()

    def to_dict(self):
        return {
            'id'      : self.id,
            'username': self.username,
            'name'    : self.name,
            'surname' : self.surname,
            'role'    : code_to_user_role(self.role),
            'tag_id'  : self.tag_id
        }
    
    def __repr__(self):
        return f'<User {self.id}>'


class AccessLog(db.Model):
    """
    A class to represent a Log in the SQLite database.
    """
    __tablename__ = 'AccessLogs'
    id        = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    tag_id    = db.Column(db.String(10), nullable=False)
    # Foreign key to Users
    user_id   = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __init__(self, user_id, tag_id):
        self.user_id = user_id
        self.tag_id  = tag_id

    @classmethod    
    def add_log(cls, user_id, tag_id):
        log = cls(user_id, tag_id)
        db.session.add(log)
        db.session.commit()
        
    @classmethod
    def retrieve_with_filters(cls, start_date=None, end_date=None, username=None):  
        if username:
            user = User.find_user(username)
            if user is None:
                raise UserNotExistException()

        if start_date and end_date and start_date >= end_date:
            raise ValueError('Invalid date range.')

        query = cls.query.with_entities(
            cls.timestamp,
            User.username,
            User.name,
            User.surname,
            cls.tag_id
        ).join(User)

        if username:
            query = query.filter_by(username=username)
        
        if start_date:
            query = query.filter(cls.timestamp >= start_date)
        
        if end_date:
            query = query.filter(cls.timestamp <= end_date)

        query = query.order_by(cls.timestamp.desc())

        logs = query.all()

        return [cls._to_dict(log) for log in logs]
    
    @staticmethod
    def _to_dict(entry):
        return {
            'timestamp': entry[0].strftime('%Y-%m-%d %H:%M:%S') \
                if isinstance(entry[0], datetime) else str(entry[0]),
            'username' : entry[1],
            'name'     : entry[2],
            'surname'  : entry[3],
            'tag_id'   : str(entry[4])
        }
        
    def __repr__(self):
        return f'<Log {self.id}>'