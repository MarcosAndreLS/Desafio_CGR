from app import create_app
from app.services.logica_negocio_service import obter_melhor_recurso

# Cria a aplicação e ativa o contexto
app = create_app()

with app.app_context():
    resultado = obter_melhor_recurso("Porta Ethernet")
    print(resultado)
