import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestOrderAPI:
    def test_customer_can_create_order(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)
        url = reverse('order-list')  # TODO: 'order-list' is the basename
        data = {
            "product_name": "Laptop",
            "quantity": 1,
            "unit_price": 1000
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert float(response.data['total_price']) == 1000

    def test_customer_only_sees_own_orders(self, api_client, customer_user, other_customer, db):
        from apps.orders.infrastructure.models.order import Order
        Order.objects.create(product_name="C1 Order", quantity=1, total_price=10, customer=customer_user)
        Order.objects.create(product_name="C2 Order", quantity=1, total_price=20, customer=other_customer)

        api_client.force_authenticate(user=customer_user)
        response = api_client.get(reverse('order-list'))

        assert len(response.data) == 1
        assert response.data[0]['product_name'] == "C1 Order"

    def test_admin_can_see_all_orders(self, api_client, admin_user, customer_user, other_customer):
        from apps.orders.infrastructure.models.order import Order
        Order.objects.create(product_name="C1", quantity=1, total_price=10, customer=customer_user)
        Order.objects.create(product_name="C2", quantity=1, total_price=20, customer=other_customer)

        api_client.force_authenticate(user=admin_user)
        response = api_client.get(reverse('order-list'))

        assert len(response.data) == 2

    def test_filter_by_price(self, api_client, admin_user, customer_user):
        from apps.orders.infrastructure.models.order import Order
        Order.objects.create(product_name="Cheap", quantity=1, total_price=50, customer=customer_user)
        Order.objects.create(product_name="Exp", quantity=1, total_price=500, customer=customer_user)

        api_client.force_authenticate(user=admin_user)
        response = api_client.get(reverse('order-list'), {'min_price': 200})

        assert len(response.data) == 1
        assert response.data[0]['product_name'] == "Exp"

    def test_customer_cannot_delete_others_order(self, api_client, customer_user, other_customer):
        from apps.orders.infrastructure.models.order import Order
        order = Order.objects.create(product_name="C2 Order", quantity=1, total_price=20, customer=other_customer)

        api_client.force_authenticate(user=customer_user)
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_total_price_is_integer(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)
        data = {
            "product_name": "Integer Test",
            "quantity": 3,
            "unit_price": 100.75
        }
        response = api_client.post(reverse('order-list'), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data['total_price'], (int, float))
        assert float(response.data['total_price']) == 302

    def test_updated_at_changes_on_partial_update(self, api_client, customer_user):
        from apps.orders.infrastructure.models.order import Order
        import time

        order = Order.objects.create(
            product_name="Initial",
            quantity=1,
            total_price=100,
            customer=customer_user
        )
        initial_update_time = order.updated_at

        time.sleep(1)

        api_client.force_authenticate(user=customer_user)
        url = reverse('order-detail', kwargs={'pk': order.id})
        api_client.patch(url, {"product_name": "Updated Name"})

        order.refresh_from_db()
        assert order.updated_at > initial_update_time

    def test_unauthorized_access_to_others_order_detail(self, api_client, other_customer, customer_user):
        from apps.orders.infrastructure.models.order import Order
        order = Order.objects.create(
            product_name="C1 Order",
            quantity=1,
            total_price=50,
            customer=customer_user
        )

        api_client.force_authenticate(user=other_customer)
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
