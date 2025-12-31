import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistrationAPI:
    def test_user_registration_success(self, api_client):
        url = reverse('register')
        data = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "StrongPassword123",
            "role": "CUSTOMER"
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="new@example.com").exists()
        assert User.objects.get(email="new@example.com").role == "CUSTOMER"

    def test_registration_fails_with_existing_email(self, api_client, customer_user):
        url = reverse('register')
        data = {
            "username": "another_user",
            "email": customer_user.email,
            "password": "Password123"
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_default_role_is_customer(self, api_client):
        url = reverse('register')
        data = {
            "username": "default_role_user",
            "email": "default@example.com",
            "password": "Password123"
        }
        api_client.post(url, data)
        user = User.objects.get(username="default_role_user")

        assert user.role == "CUSTOMER"
