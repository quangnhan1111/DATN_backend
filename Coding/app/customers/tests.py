from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


# Create your tests here.
from rolepermissions.roles import assign_role

from app.roles import Admin


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "test_user",
            "password": "123qwe!@#",
            "email": "test_user@email.com",
            "first_name": "Nhan",
            "last_name": "Nguyen",
            "address": "VN",
            "phone_number": "84796578027"
        }
        response = self.client.post("/api/v1/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CustomerViewTestCase(APITestCase):

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
        response = self.client.get('/api/v1/admin/customer/get-all')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_index(self):
        response = self.client.get('/api/v1/admin/customers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_customer(self):
        data = {
            "username": "test_user",
            "password": "123qwe!@#",
            "email": "test_user@email.com",
            "first_name": "Nhan",
            "last_name": "Nguyen",
            "address": "VN",
            "phone_number": "84796578027"
        }
        response = self.client.post('/api/v1/admin/customers', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_customer(self):
        data_add = {
            "username": "test_user",
            "password": "123qwe!@#",
            "email": "test_user@email.com",
            "first_name": "Nhan",
            "last_name": "Nguyen",
            "address": "VN",
            "phone_number": "84796578027"
        }
        self.client.post('/api/v1/admin/customers', data_add)
        data = {
            "username": "test_user1",
            "password": "123qwe!@#",
            "email": "test_user1@email.com",
            "first_name": "Nhan",
            "last_name": "Nguyen",
            "address": "VN",
            "phone_number": "84796578027"
        }
        response = self.client.put('/api/v1/admin/customers?id=2', data)
        self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_delete_customer(self):
        data_add = {
            "username": "test_user",
            "password": "123qwe!@#",
            "email": "test_user@email.com",
            "first_name": "Nhan",
            "last_name": "Nguyen",
            "address": "VN",
            "phone_number": "84796578027"
        }
        self.client.post('/api/v1/admin/customers', data_add)
        response = self.client.delete('/api/v1/admin/customers?id=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_customer(self):
        data_add = {
            "username": "test_user",
            "password": "123qwe!@#",
            "email": "test_user@email.com",
            "first_name": "Nhan",
            "last_name": "Nguyen",
            "address": "VN",
            "phone_number": "84796578027"
        }
        self.client.post('/api/v1/admin/customers', data_add)
        response = self.client.get('/api/v1/customer/4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    # def test_login(self):
    #     # login
    #     response = self.client.post('/api/v1/auth/login', self.credentials)
    #     # should be logged in now, fails however
    #     self.assertTrue(response.context['user'].is_authenticated)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
