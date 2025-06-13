import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from app.services.logica_negocio_service import verificar_gargalos, obter_melhor_recurso

class TestLogicaNegocioService(unittest.TestCase):

    @patch('app.services.logica_negocio_service.contar_eventos_offline')
    def test_verificar_gargalos_com_problema(self, mock_contar):
        # Mock para simular que tem eventos suficientes para identificar problema
        mock_contar.return_value = 5

        resultado = verificar_gargalos(equipamento_id=1, limite_eventos=3, intervalo_minutos=10)

        self.assertTrue(resultado['problema_detectado'])
        self.assertIn("5 eventos de status 'Offline'", resultado['mensagem'])

    @patch('app.services.logica_negocio_service.contar_eventos_offline')
    def test_verificar_gargalos_sem_problema(self, mock_contar):
        # Mock para simular poucos eventos, sem problema
        mock_contar.return_value = 1

        resultado = verificar_gargalos(equipamento_id=1, limite_eventos=3, intervalo_minutos=10)

        self.assertFalse(resultado['problema_detectado'])
        self.assertEqual(resultado['mensagem'], "Nenhum gargalo identificado.")

    @patch('app.services.logica_negocio_service.buscar_melhor_recurso_disponivel')
    def test_obter_melhor_recurso_existente(self, mock_buscar):
        # Simula um recurso retornado do banco
        mock_buscar.return_value = (10, 1, 'Porta Ethernet', 'Eth0/1', 'Disponível', None, '2025-06-13 10:00:00')

        resultado = obter_melhor_recurso('Porta Ethernet', equipamento_id=1)

        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['id'], 10)
        self.assertEqual(resultado['tipo_recurso'], 'Porta Ethernet')
        self.assertEqual(resultado['status_alocacao'], 'Disponível')

    @patch('app.services.logica_negocio_service.buscar_melhor_recurso_disponivel')
    def test_obter_melhor_recurso_nao_encontrado(self, mock_buscar):
        mock_buscar.return_value = None

        resultado = obter_melhor_recurso('IP v4')

        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
