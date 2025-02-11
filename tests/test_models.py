import unittest
from unittest.mock import MagicMock
from datetime import datetime
from werkzeug.utils import secure_filename

# Simulação de Models sem interação com o banco real
class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __str__(self):
        return f'<User name="{self.first_name} {self.last_name}", email="{self.email}">'

    def verify_password(self, password):
        return self.password == password

    def is_valid(self):
        valid = True
        if len(self.first_name) < 3 or len(self.first_name) > 50:
            valid = False
        if len(self.last_name) < 3 or len(self.last_name) > 50:
            valid = False
        if len(self.email) < 6 or len(self.email) > 100:
            valid = False
        if len(self.password) < 8 or len(self.password) > 254:
            valid = False
        return valid

class Video:
    def __init__(self, file, user):
        self.filename = secure_filename(file.filename)
        self.user_id = user.email
        self.upload_date = datetime.now()

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['mp4', 'avi', 'mov', 'mkv', 'm4a']

    def is_valid(self):
        return self.filename != '' and self.allowed_file(self.filename)

    def get_secure_filename(self):
        return self.filename

# Teste de Modelos
class ModelTestCase(unittest.TestCase):

    def test_user_creation(self):
        """Teste a criação de um usuário sem conectar ao banco"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="12345678")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")

    def test_user_password_verification(self):
        """Teste a verificação de senha"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="12345678")
        self.assertTrue(user.verify_password("12345678"))
        self.assertFalse(user.verify_password("wrongpassword"))

    def test_user_validity(self):
        """Teste a validade do usuário"""
        valid_user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="12345678")
        invalid_user = User(first_name="Jo", last_name="D", email="johndoe@example", password="1234")
        self.assertTrue(valid_user.is_valid())
        self.assertFalse(invalid_user.is_valid())

    def test_video_creation_with_mocked_file(self):
        """Teste a criação de um vídeo com um arquivo simulado"""
        mock_file = MagicMock()
        mock_file.filename = "some_video.mp4"
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="12345678")
        video = Video(file=mock_file, user=user)
        self.assertEqual(video.filename, "some_video.mp4")
        self.assertEqual(video.user_id, "john.doe@example.com")

    def test_video_validity(self):
        """Teste a validade do vídeo"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="12345678")
        valid_video = Video(file=MagicMock(filename="valid_video.mp4"), user=user)
        invalid_video = Video(file=MagicMock(filename="invalid_video.txt"), user=user)
        self.assertTrue(valid_video.is_valid())
        self.assertFalse(invalid_video.is_valid())

    def test_get_secure_filename(self):
        """Teste se o método get_secure_filename está funcionando"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="12345678")
        video = Video(file=MagicMock(filename="some_video.mp4"), user=user)
        self.assertEqual(video.get_secure_filename(), "some_video.mp4")

if __name__ == '__main__':
    unittest.main()
