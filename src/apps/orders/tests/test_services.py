import pytest
from unittest.mock import MagicMock
from apps.orders.application.services import OrderService
from apps.orders.domain.entities import OrderEntity


class TestOrderService:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repo):
        return OrderService(repository=mock_repo)

    def test_create_order_calculates_correct_total(self, service, mock_repo):
        mock_repo.save.side_effect = lambda x: x

        order = service.create_order(
            customer_id=1,
            product_name="Test Product",
            quantity=5,
            unit_price=10.0
        )

        assert order.total_price == 50
        assert mock_repo.save.called

    def test_get_orders_for_customer_adds_owner_filter(self, service, mock_repo):
        user = MagicMock()
        user.id = 10
        user.is_admin.return_value = False

        service.get_orders_for_user(user, {})

        args, _ = mock_repo.list_all.call_args
        assert args[0]['customer_id'] == 10

    def test_update_order_security_denies_non_owner(self, service, mock_repo):
        existing_order = OrderEntity(
            id=1, product_name="P1", quantity=1, total_price=10, customer_id=99
        )
        mock_repo.get_by_id.return_value = existing_order

        user = MagicMock()
        user.id = 10
        user.is_admin.return_value = False

        with pytest.raises(PermissionError):
            service.update_order_securely(1, user, {"product_name": "New"})
