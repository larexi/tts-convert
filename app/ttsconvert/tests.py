from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
from rest_framework.test import APIClient

class Tests(TestCase):

    def test_token_api(self):
        client = APIClient()

        User = get_user_model()
        user = User.objects.create_user(username="test", password="test")

        response = client.post('/api-token-auth/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)