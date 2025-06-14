from app.repositories.equipamentos_repository import (
    listar_todos_equipamentos,
    buscar_equipamento_por_id,
    obter_status_equipamento,
    atualizar_status_equipamento_no_banco
)
from app.services.eventos_service import registrar_evento
from app.utils.notificacoes import notificar_evento

def obter_todos_equipamentos():
    return listar_todos_equipamentos()

def obter_equipamento_por_id(equip_id):
    row = buscar_equipamento_por_id(equip_id)
    if row:
        return {
            'id': row[0],
            'nome': row[1],
            'tipo': row[2],
            'ip_gerenciamento': row[3],
            'status': row[4],
            'localizacao': row[5]
        }
    return None

def processar_atualizacao_status(equip_id, novo_status):
    try:
        status_atual = obter_status_equipamento(equip_id)

        if status_atual is None:
            return None

        if status_atual == novo_status:
            return {
                "mensagem": f"O status já está como '{novo_status}'. Nenhuma alteração foi feita."
            }

        atualizar_status_equipamento_no_banco(equip_id, novo_status)
        descricao = f"Status alterado de {status_atual} para {novo_status}."
        registrar_evento(equip_id, "Status Change", descricao)

        if novo_status.lower() == "offline":
            notificar_evento(
                tipo="Equipamento Offline",
                mensagem=f"Equipamento {equip_id} ficou offline.",
            )

        return {
            "status_alterado": True,
            "mensagem": "Status atualizado com sucesso.",
            "status_anterior": status_atual,
            "status_novo": novo_status
        }
    except Exception as e:
        return {
            "erro": f"Erro ao processar atualização de status: {str(e)}"
        }