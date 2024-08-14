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
        'host': 'mongodb+srv://admin:nnFzjCVdn68xtAic@cluster0.29ksh.mongodb.net/server_system?retryWrites=true&w=majority&appName=Cluster0'
    }

    # MQTT configuration
    MQTT_SETTINGS = {
        'addr'  : '49ded85c25e645a7ba547aee781d2231.s1.eu.hivemq.cloud',
        'port'  : 8883,
        'user'  : 'darkknight',
        'pass'  : 'ie6fLMLc2D!LVT^r##',
        'topics': {
            'intrusion': '/server/intrusion',
            'alarm'    : '/server/alarm',
            'detection': '/server/detection',
            'temp'     : '/server/temperature'
        }
    }