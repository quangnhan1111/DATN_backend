from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from rolepermissions.roles import assign_role

from app.roles import Admin


class CouponTestCase(APITestCase):

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
        response = self.client.get('/api/v1/coupon-list-no-page')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_index(self):
        response = self.client.get('/api/v1/coupons')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_coupon(self):
        data = {
            'name': 'testCoupon',
            'time': 10,
            'condition': 'PHAN_TRAM',
            'value': 10,
            'name_code': 'COVID19',
        }
        response = self.client.post('/api/v1/coupons', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_brand(self):
        data_add = {
            'name': 'testCoupon',
            'time': 10,
            'condition': 'PHAN_TRAM',
            'value': 10,
            'name_code': 'COVID19',
        }
        self.client.post('/api/v1/coupons', data_add)
        data = {
            'name': 'testCoupon1',
            'time': 12,
            'condition': 'PHAN_TRAM',
            'value': 12,
            'name_code': 'COVID19',
        }
        response = self.client.put('/api/v1/coupons?id=2', data)
        self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_delete_brand(self):
        data_add = {
            'name': 'testCoupon',
            'time': 10,
            'condition': 'PHAN_TRAM',
            'value': 10,
            'name_code': 'COVID19',
        }
        self.client.post('/api/v1/coupons', data_add)
        response = self.client.delete('/api/v1/coupons?id=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_brand(self):
        data_add = {
            'name': 'testCoupon',
            'time': 10,
            'condition': 'PHAN_TRAM',
            'value': 10,
            'name_code': 'COVID19',
        }
        self.client.post('/api/v1/coupons', data_add)
        response = self.client.get('/api/v1/coupon/4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
