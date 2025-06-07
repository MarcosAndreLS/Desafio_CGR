from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['DB_PATH'] = os.path.join(os.getcwd(), 'database', 'db.sqlite3')

    from .routes.init import init_bp
    app.register_blueprint(init_bp)

    return app
