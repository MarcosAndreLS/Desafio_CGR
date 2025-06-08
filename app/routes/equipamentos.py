from flask import Blueprint, jsonify, current_app, request
from app.models.db import get_connection

equipamentos_bp = Blueprint('equipamentos', __name__)

@equipamentos_bp.route('/equipamentos', methods=['GET'])
def listar_equipamentos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipamentos")
        rows = cursor.fetchall()

        colunas = [desc[0] for desc in cursor.description]
        equipamentos = [dict(zip(colunas, row)) for row in rows]

        return jsonify(equipamentos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()

@equipamentos_bp.route('/equipamentos/<int:equip_id>', methods=['GET'])
def buscar_equipamento_por_idd(equip_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM equipamentos WHERE id = ?', (equip_id,))
    row = cursor.fetchone()

    conn.close()

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

    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    # Verifica se equipamento existe
    cursor.execute('SELECT status FROM equipamentos WHERE id = ?', (equip_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"erro": "Equipamento não encontrado."}), 404

    status_antigo = row[0]

    # Atualiza status
    cursor.execute('UPDATE equipamentos SET status = ? WHERE id = ?', (novo_status, equip_id))

    # Insere log do evento
    descricao = f"Status alterado de '{status_antigo}' para '{novo_status}'."
    cursor.execute(
        'INSERT INTO eventos (equipamento_id, tipo_evento, descricao) VALUES (?, ?, ?)',
        (equip_id, 'Status Change', descricao)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Status atualizado com sucesso.", "novo_status": novo_status})
