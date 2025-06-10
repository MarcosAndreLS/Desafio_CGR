from flask import Blueprint, current_app
from app.models.db import init_db

init_bp = Blueprint('init', __name__)

@init_bp.route('/')
def initialize_database():
    db_path = current_app.config['DB_PATH']
    schema_path = 'database/schema.sql'
    data_path = 'database/data.sql'

    try:
        mensagem = init_db(db_path, schema_path, data_path)
        return mensagem
    except Exception as e:
        return f'Erro ao criar banco: {e}', 500
