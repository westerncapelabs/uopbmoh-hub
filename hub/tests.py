import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from .models import DummyModel


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()


class AuthenticatedAPITestCase(APITestCase):

    def setUp(self):
        super(AuthenticatedAPITestCase, self).setUp()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username,
                                             'testuser@example.com',
                                             self.password)
        token = Token.objects.create(user=self.user)
        self.token = token.key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)


class TestHubApp(AuthenticatedAPITestCase):

    def test_login(self):
        request = self.client.post(
            '/api/token-auth/',
            {"username": "testuser", "password": "testpass"})
        token = request.data.get('token', None)
        self.assertIsNotNone(
            token, "Could not receive authentication token on login post.")
        self.assertEqual(request.status_code, 200,
                         "Status code on /api/token-auth was %s (should be 200)."
                         % request.status_code)

    def test_create_clinician_data(self):
        post_data = {
            "msisdn": "+27845000001",
            "source": "TRAINING1",
            "sitename": "Hospital One Deep City Zone",
            "extra": {"a": "a", "b": 2}
        }
        response = self.client.post('/api/v1/clinician/',
                                    json.dumps(post_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        d = Clinician.objects.last()
        self.assertEqual(d.msisdn, "+27845000001")
        self.assertEqual(d.source, "TRAINING1")
        self.assertEqual(d.sitename, "Hospital One Deep City Zone")
        self.assertEqual(d.extra, {"a": "a", "b": 2})
