import random
from app.repositories.recursos_repository import atualizar_status_recurso, listar_recursos_por_equipamento

from app.services.eventos_service import registrar_evento

def simular_falha_equipamento(equipamento_id):
    recursos = listar_recursos_por_equipamento(equipamento_id)

    if not recursos:
        return {"erro": "Nenhum recurso encontrado para o equipamento."}
    
    recursos_ids = [r["id"] for r in recursos]
    print(recursos_ids)

    recursos_selecionados = random.sample(recursos_ids, min(len(recursos_ids), random.randint(1, len(recursos_ids))))

    status_possiveis = ["Com Problema", "Indisponível"]
    logs = []

    for recurso_id in recursos_selecionados:
        novo_status = random.choice(status_possiveis)
        atualizar_status_recurso(recurso_id, novo_status)

        descricao = f"Simulação de falha: status alterado para {novo_status}."
        registrar_evento(equipamento_id, "Falha Simulada", descricao)

        logs.append({"recurso_id": recurso_id, "status_simulado": novo_status})

    return {
        "equipamento_id": equipamento_id,
        "recursos_afetados": logs
    }
