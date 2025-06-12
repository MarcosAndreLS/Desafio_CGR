import random
from app.models.db import get_connection

def simular_falha_equipamento(equipamento_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Pega todos os recursos associados ao equipamento
    cursor.execute("""
        SELECT id FROM recursos
        WHERE equipamento_id = ?
    """, (equipamento_id,))
    recursos = cursor.fetchall()

    if not recursos:
        conn.close()
        return {"erro": "Nenhum recurso encontrado para o equipamento."}

    # Seleciona aleatoriamente alguns recursos para simular falha
    recursos_selecionados = random.sample(recursos, min(len(recursos), random.randint(1, len(recursos))))
    logs = []

    for (recurso_id,) in recursos_selecionados:
        novo_status = "Com Problema"
        cursor.execute("""
            UPDATE recursos
            SET status_alocacao = ?
            WHERE id = ?
        """, (novo_status, recurso_id))

        descricao = f"Simulação de falha: status alterado para '{novo_status}'."
        cursor.execute("""
            INSERT INTO eventos (equipamento_id, tipo_evento, descricao)
            VALUES (?, 'Falha Simulada', ?)
        """, (equipamento_id, descricao))

        logs.append({"recurso_id": recurso_id, "status_simulado": novo_status})

    conn.commit()
    conn.close()

    return {
        "equipamento_id": equipamento_id,
        "recursos_afetados": logs
    }
