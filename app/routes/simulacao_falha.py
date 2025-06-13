from flask import Blueprint, jsonify, request
from app.services.simulacao_falha_service import simular_falha_equipamento
from flasgger import swag_from

simulacao_falha_bp = Blueprint('simulacao_falha', __name__)

@simulacao_falha_bp.route('/equipamentos/<int:equip_id>/simular_falha', methods=['POST'])
@swag_from('../../docs/simulacao_falha/simulacao_falha.yml')
def simular_falha(equip_id):
    try:
        resultado = simular_falha_equipamento(equip_id)

        if "erro" in resultado:
            return jsonify(resultado), 404

        return jsonify({
            "mensagem": "Simulação de falha concluída com sucesso.",
            "dados": resultado
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500