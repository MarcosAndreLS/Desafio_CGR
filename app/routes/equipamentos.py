from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.repositories.simulacao_falha_repository import simular_falha_equipamento
from app.repositories.equipamentos_repository import (
    listar_todos_equipamentos,
    buscar_equipamento_por_id,
    atualizar_status_equipamento
)

equipamentos_bp = Blueprint('equipamentos', __name__)

@equipamentos_bp.route('/equipamentos', methods=['GET'])
@swag_from('../../docs/equipamentos/listar_equipamentos.yml')
def listar_equipamentos():
    try:
        equipamentos = listar_todos_equipamentos()
        return jsonify(equipamentos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@equipamentos_bp.route('/equipamentos/<int:equip_id>', methods=['GET'])
@swag_from('../../docs/equipamentos/equipamento_por_id.yml')
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

    resultado = atualizar_status_equipamento(equip_id, novo_status)

    if resultado is None:
        return jsonify({"erro": "Equipamento não encontrado."}), 404

    # Se o status não foi alterado
    if "status_novo" not in resultado:
        return jsonify(resultado), 200

    return jsonify({
        "mensagem": resultado["mensagem"],
        "status_anterior": resultado["status_anterior"],
        "novo_status": resultado["status_novo"]
    }), 200

@equipamentos_bp.route('/equipamentos/<int:equip_id>/simular_falha', methods=['POST'])
def simular_falha(equip_id):
    resultado = simular_falha_equipamento(equip_id)
    
    if "erro" in resultado:
        return jsonify(resultado), 404

    return jsonify({
        "mensagem": "Simulação de falha concluída com sucesso.",
        "dados": resultado
    }), 200