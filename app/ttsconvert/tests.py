import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class Tests(TestCase):

    def create_users(self):
        User = get_user_model()
        User.objects.create_user(username='test', password='test')
        User.objects.create_user(username='malicious', password='pass')

    def get_token(self, username='test', password='test'):
        client = APIClient()
        return client.post('/api-token-auth/', {'username': username, 'password': password})
    
    def test_token_api(self):
        self.create_users()
        response = self.get_token()
        self.assertEqual(response.status_code, 200)

    def test_tts_convert_api_authorization(self):
        self.create_users()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token false token')

        # Invalid token shouldn't have access
        response = client.post('/tts-convert/')
        self.assertEqual(response.status_code, 401)

    def test_tts_convert_api(self):
        self.create_users()
        response = self.get_token()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

        # Create a new ConversionRequest
        response = client.post('/tts-convert/', {'text_to_convert': 'Hello world'}, format='json')
        self.assertEqual(response.status_code, 201)
        cr_id = json.loads(response.content)['id']

        # Get the created ConversionRequest
        response = client.get('/tts-convert/', {'request_id': cr_id})
        self.assertEqual(response.status_code, 200)

        # Check that another user cannot access the ConversionRequest
        response = self.get_token('malicious', 'pass')
        malicious_client = APIClient()
        malicious_client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

        response = malicious_client.get('/tts-convert/', {'request_id': cr_id})
        self.assertEqual(response.status_code, 404)


        # Delete the request

        # Non-existent document
        response = client.delete('/tts-convert/', {'id': None}, format='json')
        self.assertEqual(response.status_code, 404)

        # User not associated with the document
        response = malicious_client.delete('/tts-convert/', {'id': cr_id}, format='json')
        self.assertEqual(response.status_code, 404)

        response = client.delete('/tts-convert/', {'id': cr_id}, format='json')
        self.assertEqual(response.status_code, 200)

       