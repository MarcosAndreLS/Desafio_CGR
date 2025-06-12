from app.repositories.recursos_repository import (
    listar_recursos_por_equipamento,
    buscar_recurso_disponivel,
    atualizar_status_recurso,
    buscar_status_recurso,
)
from app.services.eventos_service import registrar_evento

def obter_recursos_do_equipamento(equip_id):
    return listar_recursos_por_equipamento(equip_id)

def alocar_recurso(equipamento_id, tipo_recurso, cliente_associado=None):
    recurso = buscar_recurso_disponivel(equipamento_id, tipo_recurso)

    if not recurso:
        return None, "Nenhum recurso disponível encontrado."

    recurso_id = recurso[0]
    atualizar_status_recurso(recurso_id, "Alocado", cliente_associado)

    descricao = f"Recurso {recurso_id} alocado ao cliente {cliente_associado}." if cliente_associado else f"Recurso ID {recurso_id} alocado."

    registrar_evento(equipamento_id, 'Resource Allocated', descricao)

    return recurso_id, None

def desalocar_recurso(recurso_id):
    status_info = buscar_status_recurso(recurso_id)

    if not status_info:
        return {"erro": "Recurso não encontrado."}, 404

    equipamento_id, status_alocacao = status_info

    if status_alocacao != "Alocado":
        return {"erro": "Recurso não está alocado."}, 400

    atualizar_status_recurso(recurso_id, "Disponível")

    registrar_evento(equipamento_id, 'Resource Deallocated', f"Recurso {recurso_id} desalocado com sucesso.")

    return {"mensagem": "Recurso desalocado com sucesso."}, 200
