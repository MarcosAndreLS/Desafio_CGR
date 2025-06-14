from app.models.db import get_connection
from flask import current_app

# Retorna todos os recursos associados a um equipamento específico
def listar_recursos_por_equipamento(equip_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tipo_recurso, valor_recurso, status_alocacao, cliente_associado
        FROM recursos
        WHERE equipamento_id = ?
    """, (equip_id,))
    rows = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]
    recursos = [dict(zip(colunas, row)) for row in rows]

    conn.close()
    return recursos

# Busca um recurso disponível de um tipo específico em um equipamento
def buscar_recurso_disponivel(equipamento_id, tipo_recurso):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM recursos
        WHERE equipamento_id = ? AND tipo_recurso = ? AND status_alocacao = 'Disponível'
        LIMIT 1
    """, (equipamento_id, tipo_recurso))
    recurso = cursor.fetchone()

    conn.close()
    return recurso

# Atualiza o status de alocação de um recurso, cliente associado e a data de atualização
def atualizar_status_recurso(recurso_id, novo_status, cliente_associado=None):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE recursos
        SET status_alocacao = ?,
            cliente_associado = ?,
            status_atualizado_em = datetime('now', '-3 hours')
        WHERE id = ?
    """, (novo_status, cliente_associado, recurso_id))

    conn.commit()
    conn.close()

# Retorna o equipamento e o status de alocação de um recurso específico
def buscar_status_recurso(recurso_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("SELECT equipamento_id, status_alocacao FROM recursos WHERE id = ?", (recurso_id,))
    row = cursor.fetchone()

    conn.close()
    return row
