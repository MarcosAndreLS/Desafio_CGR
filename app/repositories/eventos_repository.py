from app.models.db import get_connection
from flask import current_app

# Retorna todos os logs de eventos, incluindo nome do equipamento relacionado, ordenados por data (mais recentes primeiro)
def buscar_todos_logs():
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.equipamento_id, eq.nome as nome_equipamento, e.timestamp, e.tipo_evento, e.descricao
        FROM eventos e
        LEFT JOIN equipamentos eq ON e.equipamento_id = eq.id
        ORDER BY e.timestamp DESC
    """)
    rows = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]
    logs = [dict(zip(colunas, row)) for row in rows]
    conn.close()
    return logs

# Insere um novo evento (log) relacionado a um equipamento no banco de dados
def inserir_evento(equipamento_id, tipo_evento, descricao):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO eventos (equipamento_id, tipo_evento, descricao)
        VALUES (?, ?, ?)
    """, (equipamento_id, tipo_evento, descricao))

    conn.commit()
    conn.close()