from flask import Blueprint, jsonify, request
from app.repositories.equipamentos_repository import (
    listar_todos_equipamentos,
    buscar_equipamento_por_id,
    atualizar_status_equipamento
)

equipamentos_bp = Blueprint('equipamentos', __name__)

@equipamentos_bp.route('/equipamentos', methods=['GET'])
def listar_equipamentos():
    try:
        equipamentos = listar_todos_equipamentos()
        return jsonify(equipamentos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@equipamentos_bp.route('/equipamentos/<int:equip_id>', methods=['GET'])
def buscar_equipamento_por_idd(equip_id):
    row = buscar_equipamento_por_id(equip_id)
    if row:
        equipamento = {
            'id': row[0],
            'nome': row[1],
            'tipo': row[2],
            'ip_gerenciamento': row[3],
            'status': row[4],
            'localizacao': row[5]
        }
        return jsonify(equipamento)
    else:
        return jsonify({'erro': 'Equipamento não encontrado'}), 404

@equipamentos_bp.route('/equipamentos/<int:equip_id>/status', methods=['PUT'])
def atualizar_status(equip_id):
    data = request.get_json()
    novo_status = data.get('status')

    if not novo_status:
        return jsonify({"erro": "Campo 'status' é obrigatório."}), 400

    status = atualizar_status_equipamento(equip_id, novo_status)
    if status is None:
        return jsonify({"erro": "Equipamento não encontrado."}), 404

    return jsonify({"mensagem": "Status atualizado com sucesso.", "novo_status": status})
