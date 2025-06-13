import unittest
from unittest.mock import patch
from app import create_app
import json

class EquipamentosRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.routes.equipamentos.obter_todos_equipamentos')
    def test_listar_equipamentos(self, mock_obter_todos):
        # Mock retorna lista simulada
        mock_obter_todos.return_value = [
            {'id': 1, 'nome': 'Equip 1', 'tipo': 'Tipo A', 'ip_gerenciamento': '10.0.0.1', 'status': 'Disponível', 'localizacao': 'Sala 1'},
            {'id': 2, 'nome': 'Equip 2', 'tipo': 'Tipo B', 'ip_gerenciamento': '10.0.0.2', 'status': 'Offline', 'localizacao': 'Sala 2'}
        ]

        response = self.client.get('/equipamentos')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['nome'], 'Equip 1')

    @patch('app.routes.equipamentos.obter_equipamento_por_id')
    def test_buscar_equipamento_por_id_sucesso(self, mock_obter_por_id):
        mock_obter_por_id.return_value = {
            'id': 1,
            'nome': 'Switch A',
            'tipo': 'Switch',
            'ip_gerenciamento': '192.168.0.1',
            'status': 'Disponível',
            'localizacao': 'Sala X'
        }

        response = self.client.get('/equipamentos/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['status'], 'Disponível')

    @patch('app.routes.equipamentos.obter_equipamento_por_id')
    def test_buscar_equipamento_por_id_nao_encontrado(self, mock_obter_por_id):
        mock_obter_por_id.return_value = None

        response = self.client.get('/equipamentos/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertEqual(data['erro'], 'Equipamento não encontrado')

    @patch('app.routes.equipamentos.processar_atualizacao_status')
    def test_atualizar_status_sucesso(self, mock_processar):
        mock_processar.return_value = {
            "mensagem": "Status atualizado com sucesso.",
            "status_anterior": "Disponível",
            "status_novo": "Manutenção"
        }

        response = self.client.put(
            '/equipamentos/1/status',
            data=json.dumps({"status": "Manutenção"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('mensagem', data)
        self.assertEqual(data['novo_status'], 'Manutenção')

    @patch('app.routes.equipamentos.processar_atualizacao_status')
    def test_atualizar_status_sem_status(self, mock_processar):
        # Não precisa mockar porque a requisição é barrada antes de chamar
        response = self.client.put(
            '/equipamentos/1/status',
            data=json.dumps({}),  # sem 'status'
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn("Campo 'status' é obrigatório", data['erro'] or data['erro'])

    @patch('app.routes.equipamentos.processar_atualizacao_status')
    def test_atualizar_status_equipamento_nao_encontrado(self, mock_processar):
        mock_processar.return_value = None

        response = self.client.put(
            '/equipamentos/999/status',
            data=json.dumps({"status": "Manutenção"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertEqual(data['erro'], 'Equipamento não encontrado.')

    @patch('app.routes.equipamentos.processar_atualizacao_status')
    def test_atualizar_status_erro(self, mock_processar):
        mock_processar.return_value = {"erro": "Erro inesperado"}

        response = self.client.put(
            '/equipamentos/1/status',
            data=json.dumps({"status": "Manutenção"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('erro', data)

if __name__ == '__main__':
    unittest.main()
