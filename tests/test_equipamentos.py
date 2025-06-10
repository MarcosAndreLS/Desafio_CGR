import unittest
import os
from app import create_app
from app.models.db import init_db

class EquipamentosTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Caminhos dos arquivos
        db_path = self.app.config['DB_PATH']
        schema_path = 'database/schema.sql'
        data_path = 'database/data.sql'

        # Garante um banco limpo
        init_db(db_path, schema_path, data_path)

    def test_get_equipamentos(self):
        response = self.client.get('/equipamentos')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
