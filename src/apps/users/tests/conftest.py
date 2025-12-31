import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def customer_user(db):
    return User.objects.create_user(
        username="customer1",
        email="customer1@example.com",
        password="Password123",
        role="CUSTOMER"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username="admin1",
        email="admin1@example.com",
        password="Password123",
        role="ADMIN",
        is_staff=True
    )


@pytest.fixture
def other_customer(db):
    return User.objects.create_user(
        username="customer2",
        email="customer2@example.com",
        password="Password123",
        role="CUSTOMER"
    )
