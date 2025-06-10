from flask import Blueprint, jsonify
from app.repositories.eventos_repository import listar_todos_logs

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/logs', methods=['GET'])
def listar_logs():
    try:
        logs = listar_todos_logs()
        return jsonify(logs)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
