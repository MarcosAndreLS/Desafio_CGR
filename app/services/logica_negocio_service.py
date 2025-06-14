from datetime import datetime, timedelta, timezone
from app.repositories.logica_negocio_repository import (
    contar_eventos_problema, 
    buscar_melhor_recurso_disponivel
)

def verificar_gargalos(equipamento_id, limite_eventos=3, intervalo_minutos=10):
    utc_minus_3 = timezone(timedelta(hours=-3))
    tempo_limite = (datetime.now(utc_minus_3) - timedelta(minutes=intervalo_minutos)).strftime("%Y-%m-%d %H:%M:%S")

    quantidade = contar_eventos_problema(equipamento_id, tempo_limite)

    if quantidade >= limite_eventos:
        return {
            "equipamento_id": equipamento_id,
            "problema_detectado": True,
            "mensagem": f"{quantidade} eventos de status crítico ('Offline', 'Com Problema' ou 'Indisponível') nos últimos {intervalo_minutos} minutos."
        }
    else:
        return {
            "equipamento_id": equipamento_id,
            "problema_detectado": False,
            "mensagem": "Nenhum gargalo identificado."
        }

def obter_melhor_recurso(tipo_recurso, equipamento_id=None):
    recurso = buscar_melhor_recurso_disponivel(tipo_recurso, equipamento_id)
    if recurso:
        colunas = ['id', 'equipamento_id', 'tipo_recurso', 'valor_recurso', 'status_alocacao', 'cliente_associado',  'status_atualizado_em']
        return dict(zip(colunas, recurso))
    else:
        return None
