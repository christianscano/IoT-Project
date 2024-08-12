from flask import Flask
from .models.sqlite import User
from .db import sqlite_db, mongo_db
from .apis import api, api_user

app = Flask(__name__)

app.config.from_object('config.Config')

# Initialize SQLite
sqlite_db.init_app(app)
with app.app_context():
    sqlite_db.create_all()

    if not User.query.filter_by(name='admin').first():
        User.create_user('admin', 'admin', 'admin', 'admin', 'admin')

# Initialize MongoDB
mongo_db.init_app(app)

app.register_blueprint(api, url_prefix='/api/v1')

app.run(host='0.0.0.0', port=5000)