from flask import Blueprint, jsonify, request

from app.services.logica_negocio_service import (
    verificar_gargalos, 
    obter_melhor_recurso
)

logica_negocio_bp = Blueprint('logica_negocio', __name__)

@logica_negocio_bp.route('/equipamentos/<int:equip_id>/verificar_gargalos', methods=['GET'])
def verificar_gargalos_equipamento(equip_id):
    try:
        resultado = verificar_gargalos(equip_id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@logica_negocio_bp.route('/recursos/melhor', methods=['GET'])
def melhor_recurso():
    tipo_recurso = request.args.get('tipo_recurso')
    equipamento_id = request.args.get('equipamento_id')

    if not tipo_recurso:
        return jsonify({"erro": "O parâmetro 'tipo_recurso' é obrigatório."}), 400

    try:
        equipamento_id = int(equipamento_id) if equipamento_id else None
    except ValueError:
        return jsonify({"erro": "O parâmetro 'equipamento_id' deve ser um número inteiro."}), 400

    recurso = obter_melhor_recurso(tipo_recurso, equipamento_id)

    if recurso:
        return jsonify(recurso), 200
    else:
        return jsonify({"mensagem": "Nenhum recurso disponível encontrado."}), 404