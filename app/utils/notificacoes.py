def notificar_evento(tipo, mensagem, dados=None):
    """Função genérica de notificação (atualmente apenas imprime no console)."""
    print(f"[NOTIFICAÇÃO] Tipo: {tipo}")
    print(f"Mensagem: {mensagem}")
    if dados:
        print(f"Dados adicionais: {dados}")