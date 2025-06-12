from flask import Blueprint, jsonify
from app.services.eventos_service import listar_logs

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/logs', methods=['GET'])
def listar_logs_endpoint():
    try:
        logs = listar_logs()
        return jsonify(logs)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
