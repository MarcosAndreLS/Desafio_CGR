from app.models.db import get_connection
from flask import current_app
from app.repositories.eventos_repository import registrar_evento

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
    # Se o status já for o mesmo, não faz nada
    if status_antigo == novo_status:
        conn.close()
        return {
            "mensagem": f"O status já está como '{novo_status}'. Nenhuma alteração foi feita."
        }

    cursor.execute("UPDATE equipamentos SET status = ? WHERE id = ?", (novo_status, equip_id))
    descricao = f"Status alterado de {status_antigo} para {novo_status}."
    registrar_evento(conn, equip_id, "Status Change", descricao)

    conn.commit()
    conn.close()
    return {
        "status_alterado": True,
        "mensagem": "Status atualizado com sucesso.",
        "status_anterior": status_antigo,
        "status_novo": novo_status
    }
