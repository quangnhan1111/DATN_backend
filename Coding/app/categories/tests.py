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

    def test_get_list_no_paginate(self):
        response = self.client.get('/api/v1/categories-list-no-page')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_index(self):
        response = self.client.get('/api/v1/categories')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_category(self):
        data = {
            "name": "testCategory",
        }
        response = self.client.post('/api/v1/categories', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_category(self):
        data_add = {
            "name": "testCategory",
        }
        self.client.post('/api/v1/categories', data_add)
        data_change = {
            "name": "changeCategory",
        }
        response = self.client.put('/api/v1/categories?id=2', data_change)
        self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_delete_category(self):
        data_add = {
            "name": "testCategory",
        }
        self.client.post('/api/v1/categories', data_add)
        response = self.client.delete('/api/v1/categories?id=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_customer(self):
        data_add = {
            "name": "testCategory",
        }
        self.client.post('/api/v1/categories', data_add)
        response = self.client.get('/api/v1/category/4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
