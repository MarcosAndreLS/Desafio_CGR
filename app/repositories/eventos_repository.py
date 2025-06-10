from app.models.db import get_connection
from flask import current_app

def listar_todos_logs():
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