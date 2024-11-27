from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
from rest_framework.test import APIClient

class Tests(TestCase):

    def create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="test", password="test")

    def get_token(self):
        client = APIClient()
        return client.post('/api-token-auth/', {'username': 'test', 'password': 'test'})

    def test_token_api(self):
        self.create_user()
        response = self.get_token()
        self.assertEqual(response.status_code, 200)

    def test_tts_convert_api(self):
        self.create_user()
        response = self.get_token()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')
        response = client.get('/tts-convert/')
        self.assertEqual(response.status_code, 200)