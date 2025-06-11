from app import create_app
from app.repositories.logica_negocio_repository import get_melhor_recurso_disponivel

# Cria a aplicação e ativa o contexto
app = create_app()

with app.app_context():
    resultado = get_melhor_recurso_disponivel("Porta Ethernet")
    print(resultado)
