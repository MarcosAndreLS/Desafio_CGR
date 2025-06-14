from app.models.db import get_connection
from flask import current_app

# Retorna todos os equipamentos cadastrados na tabela 'equipamentos'
def listar_todos_equipamentos():
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM equipamentos")
    rows = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]
    equipamentos = [dict(zip(colunas, row)) for row in rows]

    conn.close()
    return equipamentos


# Busca um equipamento específico pelo ID
def buscar_equipamento_por_id(equip_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM equipamentos WHERE id = ?", (equip_id,))
    row = cursor.fetchone()

    conn.close()
    return row

# Retorna o status atual de um equipamento pelo ID
def obter_status_equipamento(equip_id):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM equipamentos WHERE id = ?", (equip_id,))
    row = cursor.fetchone()

    conn.close()
    return row[0] if row else None

# Atualiza o status de um equipamento no banco de dados
def atualizar_status_equipamento_no_banco(equip_id, novo_status):
    conn = get_connection(current_app.config['DB_PATH'])
    cursor = conn.cursor()

    cursor.execute("UPDATE equipamentos SET status = ? WHERE id = ?", (novo_status, equip_id))

    conn.commit()
    conn.close()
