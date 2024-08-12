import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # General configuration
    DEBUG        = True
    SECRET_KEY   = os.urandom(32)
    CSRF_ENABLED = True

    # SQLite3 configuration
    SQLALCHEMY_DATABASE_URI        = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB configuration
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://admin:nnFzjCVdn68xtAic@cluster0.29ksh.mongodb.net/measurements?retryWrites=true&w=majority&appName=Cluster0',
    }