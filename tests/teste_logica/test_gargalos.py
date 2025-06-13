from app import create_app
from app.services.logica_negocio_service import verificar_gargalos

# Cria a aplicação e ativa o contexto
app = create_app()

with app.app_context():
    resultado = verificar_gargalos(equipamento_id=1)
    print(resultado)
