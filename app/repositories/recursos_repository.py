from app.models.db import get_connection
from flask import current_app

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

def alocar_recurso(equipamento_id, tipo_recurso, cliente_associado=None):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    # Busca um recurso disponível
    cursor.execute("""
        SELECT id FROM recursos
        WHERE equipamento_id = ? AND tipo_recurso = ? AND status_alocacao = 'Disponível'
        LIMIT 1
    """, (equipamento_id, tipo_recurso))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None, "Nenhum recurso disponível encontrado."

    recurso_id = row[0]

    # Atualiza o status do recurso para 'Alocado'
    cursor.execute("""
        UPDATE recursos
        SET status_alocacao = 'Alocado', cliente_associado = ?
        WHERE id = ?
    """, (cliente_associado, recurso_id))

    # Insere log do evento
    descricao = f"Recurso {recurso_id} alocado ao cliente '{cliente_associado}'." if cliente_associado else f"Recurso ID {recurso_id} alocado."
    cursor.execute("""
        INSERT INTO eventos (equipamento_id, tipo_evento, descricao)
        VALUES (?, 'Resource Allocated', ?)
    """, (equipamento_id, descricao))

    conn.commit()
    conn.close()

    return recurso_id, None

def desalocar_recurso(recurso_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    # Verifica se o recurso existe e está alocado
    cursor.execute(
        "SELECT equipamento_id, status_alocacao FROM recursos WHERE id = ?",
        (recurso_id,)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"erro": "Recurso não encontrado."}, 404

    equipamento_id, status_atual = row

    if status_atual != "Alocado":
        conn.close()
        return {"erro": "Recurso não está alocado."}, 400

    # Atualiza status e limpa cliente
    cursor.execute("""
        UPDATE recursos
        SET status_alocacao = 'Disponível', cliente_associado = NULL
        WHERE id = ?
    """, (recurso_id,))

    # Registra evento
    descricao = f"Recurso {recurso_id} desalocado com sucesso."
    cursor.execute("""
        INSERT INTO eventos (equipamento_id, tipo_evento, descricao)
        VALUES (?, 'Resource Deallocated', ?)
    """, (equipamento_id, descricao))

    conn.commit()
    conn.close()

    return {"mensagem": "Recurso desalocado com sucesso."}, 200
