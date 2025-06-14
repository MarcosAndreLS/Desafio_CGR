import random
from app.repositories.recursos_repository import atualizar_status_recurso, listar_recursos_por_equipamento

from app.services.eventos_service import registrar_evento

def simular_falha_equipamento(equipamento_id):
    recursos = listar_recursos_por_equipamento(equipamento_id)

    if not recursos:
        return {"erro": "Nenhum recurso encontrado para o equipamento."}
    
    recursos_selecionados = random.sample(
        recursos, 
        min(len(recursos), random.randint(1, len(recursos)))
    )

    status_possiveis = ["Com Problema", "Indisponível"]
    logs = []

    for recurso in recursos_selecionados:
        recurso_id = recurso["id"]
        cliente_atual = recurso.get("cliente_associado")  

        novo_status = random.choice(status_possiveis)

        # Atualiza o status preservando o cliente
        atualizar_status_recurso(recurso_id, novo_status, cliente_atual)

        descricao = f"Simulação de falha: status alterado para {novo_status}."
        registrar_evento(equipamento_id, "Falha Simulada", descricao)

        logs.append({
            "recurso_id": recurso_id,
            "status_simulado": novo_status,
            "cliente_preservado": cliente_atual
        })

    return {
        "equipamento_id": equipamento_id,
        "recursos_afetados": logs
    }
