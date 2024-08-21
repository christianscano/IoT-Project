from flask import Flask
from .models.sqlite import User
from .db import sqlite_db, mongo_db
from .mqtt import mqtt_handler
from .models.mongo import IntrusionSystem
from .apis import api
from .frontend.pages import front

app = Flask(__name__, static_folder=None)

app.config.from_object('config.Config')

# Initialize SQLite
sqlite_db.init_app(app)
with app.app_context():
    sqlite_db.create_all()

    if not User.query.filter_by(name='admin').first():
        User.create_user('admin', 'admin', 'admin', 'admin', 'admin')

# Initialize MongoDB
mongo_db.init_app(app)

if IntrusionSystem.get_intrusion_system() is None:
    IntrusionSystem.create_intrusion_system()

# # Inizialize MQTT
mqtt_handler.init_mqtt(app)

app.register_blueprint(api, url_prefix='/api/v1')
app.register_blueprint(front, url_prefix='/')

app.run(host='0.0.0.0', port=5000)