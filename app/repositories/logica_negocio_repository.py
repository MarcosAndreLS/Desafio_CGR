from app.models.db import get_connection

# Busca o melhor recurso disponível do tipo especificado, opcionalmente filtrando por equipamento
# Retorna o recurso disponível há mais tempo (com base em 'status_atualizado_em')
def buscar_melhor_recurso_disponivel(tipo_recurso, equipamento_id=None):
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

def contar_eventos_problema(equipamento_id, tempo_limite):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM eventos
        WHERE equipamento_id = ?
        AND tipo_evento IN ('Status Change', 'Falha Simulada')
        AND (
            descricao LIKE '%para Offline%' OR
            descricao LIKE '%para Com Problema%' OR
            descricao LIKE '%para Indisponível%'
        )
        AND timestamp >= ?
    """, (equipamento_id, tempo_limite))

    quantidade = cursor.fetchone()[0]
    conn.close()
    return quantidade
