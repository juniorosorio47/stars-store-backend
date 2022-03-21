import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User
from .serializers import UserSerializer

# class RegistrationTestCase(APITestCase):
#     def test_register(self):
#         data = {
#             "name":"Junior",
#             "email":"juniorosorio47@gmail.com", 
#             "password":"123456", 
#             "password_confirm":"123456"
#         }

#         response = self.client.post("/api/users/register/", data)

#         self.assertEqual(response.status_code,  status.HTTP_201_CREATED)
#         pass

class LoginTestCase(APITestCase):
    def test_login(self):
        data = {
            "email":"juniorosorio46@gmail.com",
            "password":"123456",
        }

        response = self.client.post("/api/users/login/", data)

        print(response.json)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        pass
