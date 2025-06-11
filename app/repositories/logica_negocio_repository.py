from app.models.db import get_connection

def get_melhor_recurso_disponivel(tipo_recurso, equipamento_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if equipamento_id:
        cursor.execute("""
            SELECT * FROM recursos
            WHERE tipo_recurso = ?
              AND equipamento_id = ?
              AND status_alocacao = 'Disponível'
              AND status_atualizado_em IS NOT NULL
            ORDER BY datetime(status_atualizado_em) ASC
            LIMIT 1;
        """, (tipo_recurso, equipamento_id))
    else:
        cursor.execute("""
            SELECT * FROM recursos
            WHERE tipo_recurso = ?
              AND status_alocacao = 'Disponível'
              AND status_atualizado_em IS NOT NULL
            ORDER BY datetime(status_atualizado_em) ASC
            LIMIT 1;
        """, (tipo_recurso,))

    recurso = cursor.fetchone()
    conn.close()
    return recurso
