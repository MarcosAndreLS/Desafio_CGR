from app.models.db import get_connection
from datetime import datetime, timedelta, timezone


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


def verificar_gargalos(equipamento_id, limite_eventos=3, intervalo_minutos=10):
    conn = get_connection()
    cursor = conn.cursor()

    # Define o timestamp do limite inferior
    tempo_limite = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()

    # Filtra eventos com tipo "Status Changed" e descrição com "Offline"
    cursor.execute("""
        SELECT COUNT(*) FROM eventos
        WHERE equipamento_id = ?
        AND tipo_evento = 'Status Changed'
        AND descricao LIKE '%para ''Offline''%'
        AND timestamp >= ?
    """, (equipamento_id, tempo_limite))

    quantidade = cursor.fetchone()[0]
    conn.close()

    if quantidade >= limite_eventos:
        return {
            "equipamento_id": equipamento_id,
            "problema_detectado": True,
            "mensagem": f"{quantidade} eventos de status 'Offline' nos últimos {intervalo_minutos} minutos."
        }
    else:
        return {
            "equipamento_id": equipamento_id,
            "problema_detectado": False,
            "mensagem": "Nenhum gargalo identificado."
        }

