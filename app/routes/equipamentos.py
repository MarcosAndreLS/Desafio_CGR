from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services.equipamentos_service import (
    obter_todos_equipamentos,
    obter_equipamento_por_id,
    processar_atualizacao_status
)

equipamentos_bp = Blueprint('equipamentos', __name__)

@equipamentos_bp.route('/equipamentos', methods=['GET'])
@swag_from('../../docs/equipamentos/listar_equipamentos.yml')
def listar_equipamentos():
    try:
        equipamentos = obter_todos_equipamentos()
        return jsonify(equipamentos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@equipamentos_bp.route('/equipamentos/<int:equip_id>', methods=['GET'])
@swag_from('../../docs/equipamentos/equipamento_por_id.yml')
def buscar_equipamento_por_idd(equip_id):
    equipamento = obter_equipamento_por_id(equip_id)
    if equipamento:
        return jsonify(equipamento)
    else:
        return jsonify({'erro': 'Equipamento não encontrado'}), 404

@equipamentos_bp.route('/equipamentos/<int:equip_id>/status', methods=['PUT'])
def atualizar_status(equip_id):
    data = request.get_json()
    novo_status = data.get('status')

    if not novo_status:
        return jsonify({"erro": "Campo 'status' é obrigatório."}), 400

    resultado = processar_atualizacao_status(equip_id, novo_status)

    if resultado is None:
        return jsonify({"erro": "Equipamento não encontrado."}), 404

    if "status_novo" not in resultado:
        return jsonify(resultado), 200

    return jsonify({
        "mensagem": resultado["mensagem"],
        "status_anterior": resultado["status_anterior"],
        "novo_status": resultado["status_novo"]
    }), 200

