from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services.recursos_service import (
    obter_recursos_do_equipamento,
    alocar_recurso,
    desalocar_recurso
)

recursos_bp = Blueprint('recursos', __name__)

@recursos_bp.route('/equipamentos/<int:equip_id>/recursos', methods=['GET'])
@swag_from('../../docs/recursos/listar_recursos_do_equipamento.yml')
def listar_recursos_do_equipamento(equip_id):
    try:
        recursos = obter_recursos_do_equipamento(equip_id)
        if not recursos:
            return jsonify({'mensagem': 'Nenhum recurso encontrado para este equipamento.'}), 404
        return jsonify(recursos)
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar recursos: {str(e)}'}), 500

@recursos_bp.route('/recursos/alocar', methods=['POST'])
@swag_from('../../docs/recursos/alocar_recurso.yml')
def alocar_recurso_endpoint():
    try:
        data = request.get_json()
        equipamento_id = data.get('equipamento_id')
        tipo_recurso = data.get('tipo_recurso')
        cliente_associado = data.get('cliente_associado')

        if not equipamento_id or not tipo_recurso:
            return jsonify({'erro': "Campos 'equipamento_id' e 'tipo_recurso' são obrigatórios."}), 400

        recurso_id, erro = alocar_recurso(equipamento_id, tipo_recurso, cliente_associado)

        if erro:
            return jsonify({'erro': erro}), 404

        return jsonify({
            'mensagem': 'Recurso alocado com sucesso.',
            'recurso_id': recurso_id,
            'cliente_associado': cliente_associado
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao alocar recurso: {str(e)}'}), 500

@recursos_bp.route('/recursos/desalocar', methods=['POST'])
@swag_from('../../docs/recursos/desalocar_recurso.yml')
def desalocar():
    try:
        data = request.get_json()
        recurso_id = data.get("recurso_id")

        if not recurso_id:
            return jsonify({"erro": "Campo 'recurso_id' é obrigatório."}), 400

        resultado, status = desalocar_recurso(recurso_id)
        return jsonify(resultado), status
    except Exception as e:
        return jsonify({'erro': f'Erro ao desalocar recurso: {str(e)}'}), 500
