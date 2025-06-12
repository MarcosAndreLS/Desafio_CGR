from app.repositories.eventos_repository import (
    buscar_todos_logs,
    inserir_evento
)

def listar_logs():
    return buscar_todos_logs()

def registrar_evento(equipamento_id, tipo_evento, descricao):
    inserir_evento(equipamento_id, tipo_evento, descricao)