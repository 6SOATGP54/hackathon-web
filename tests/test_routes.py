import unittest
from vimg import app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Configuração para rodar o app em modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home(self):
        # Testa a rota home
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Testa a rota login
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Testa a rota logout
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_signup_get(self):
        # Testa a rota signup (GET)
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        # Testa a rota signup (POST)
        response = self.client.post('/signup')
        self.assertEqual(response.status_code, 200)

    def test_upload_get(self):
        # Testa a rota upload (GET)
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        # Testa a rota upload (POST)
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
