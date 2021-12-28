from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from rolepermissions.roles import assign_role

from app.roles import Admin


class CategoryTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='adminTest', password='secret')
        assign_role(self.user, Admin)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client = APIClient()
        self.client.login(username='adminTest', password='secret')
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_messages_page(self):
        User.objects.create_user(username='staffTest', password='secret')
        data = {
            "chat_room": "TestChatRoom",
            "username": "testUserName",
            "message": "testMessage",
            "user_id": 2
        }
        response = self.client.post('/api/v1/chat', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_index(self):
    #     response = self.client.get('/api/v1/categories')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_add_category(self):
    #     data = {
    #         "name": "testCategory",
    #     }
    #     response = self.client.post('/api/v1/categories', data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_change_category(self):
    #     data = {
    #         "name": "testCategory",
    #     }
    #     response = self.client.post('/api/v1/categories?id=1', data)
    #     self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)
    #
    # def test_delete_category(self):
    #     response = self.client.delete('/api/v1/categories?id=1')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_get_detail_customer(self):
    #     response = self.client.get('/api/v1/category?id=1')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
