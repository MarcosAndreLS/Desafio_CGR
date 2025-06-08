from app.models.db import get_connection
from flask import current_app

def listar_todos_equipamentos():
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipamentos")
    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    equipamentos = [dict(zip(colunas, row)) for row in rows]
    conn.close()
    return equipamentos

def buscar_equipamento_por_id(equip_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipamentos WHERE id = ?", (equip_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def atualizar_status_equipamento(equip_id, novo_status):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM equipamentos WHERE id = ?", (equip_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    status_antigo = row[0]
    cursor.execute("UPDATE equipamentos SET status = ? WHERE id = ?", (novo_status, equip_id))
    descricao = f"Status alterado de '{status_antigo}' para '{novo_status}'."
    cursor.execute(
        "INSERT INTO eventos (equipamento_id, tipo_evento, descricao) VALUES (?, ?, ?)",
        (equip_id, "Status Change", descricao)
    )
    conn.commit()
    conn.close()
    return novo_status
