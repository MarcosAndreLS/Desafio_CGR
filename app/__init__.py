from flask import Flask
import os
from app.models.db import init_db

def create_app():
    app = Flask(__name__)
    app.config['DB_PATH'] = os.path.join(os.getcwd(), 'database', 'db.sqlite3')

    from .routes.init import init_bp
    app.register_blueprint(init_bp)

    from .routes.equipamentos import equipamentos_bp
    app.register_blueprint(equipamentos_bp)

    from .routes.recursos import recursos_bp
    app.register_blueprint(recursos_bp)

    from .routes.eventos import eventos_bp
    app.register_blueprint(eventos_bp)

    # Inicializa banco ao iniciar app
    schema_path = os.path.join(os.getcwd(), 'database', 'schema.sql')
    data_path = os.path.join(os.getcwd(), 'database', 'data.sql')
    try:
        init_db(app.config['DB_PATH'], schema_path, data_path)
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")

    return app
