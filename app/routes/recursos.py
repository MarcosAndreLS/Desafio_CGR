from flask import Blueprint, jsonify, request
from app.services.recursos_service import (
    obter_recursos_do_equipamento,
    alocar_recurso,
    desalocar_recurso
)

recursos_bp = Blueprint('recursos', __name__)

@recursos_bp.route('/equipamentos/<int:equip_id>/recursos', methods=['GET'])
def listar_recursos_do_equipamento(equip_id):
    recursos = obter_recursos_do_equipamento(equip_id)
    if not recursos:
        return jsonify({'mensagem': 'Nenhum recurso encontrado para este equipamento.'}), 404
    return jsonify(recursos)

@recursos_bp.route('/recursos/alocar', methods=['POST'])
def alocar_recurso_endpoint():
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

@recursos_bp.route('/recursos/desalocar', methods=['POST'])
def desalocar():
    data = request.get_json()
    recurso_id = data.get("recurso_id")

    if not recurso_id:
        return jsonify({"erro": "Campo 'recurso_id' é obrigatório."}), 400

    resultado, status = desalocar_recurso(recurso_id)
    return jsonify(resultado), status
