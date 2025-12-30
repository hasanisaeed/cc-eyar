import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='password123',
        role='ADMIN'
    )


@pytest.fixture
def customer_user(db):
    return User.objects.create_user(
        username='customer1',
        email='c1@test.com',
        password='password123',
        role='CUSTOMER'
    )


@pytest.fixture
def other_customer(db):
    return User.objects.create_user(
        username='customer2',
        email='c2@test.com',
        password='password123',
        role='CUSTOMER'
    )
