from typing import List, Optional
from django.utils import timezone
from apps.orders.domain.entities import OrderEntity
from apps.orders.domain.repositories import OrderRepositoryInterface
from apps.orders.infrastructure.models.order import Order


class DjangoOrderRepository(OrderRepositoryInterface):
    def _to_entity(self, instance: Order) -> OrderEntity:
        return OrderEntity(
            id=instance.id,
            product_name=instance.product_name,
            quantity=instance.quantity,
            total_price=instance.total_price,
            customer_id=instance.customer_id,
            created_at=instance.created_at,
            updated_at=instance.updated_at
        )

    def save(self, entity: OrderEntity) -> OrderEntity:
        if entity.id:
            Order.objects.filter(id=entity.id).update(
                product_name=entity.product_name,
                quantity=entity.quantity,
                total_price=entity.total_price,
                customer_id=entity.customer_id,
                updated_at=timezone.now()
            )
            obj = Order.objects.get(id=entity.id)
        else:
            obj = Order.objects.create(
                product_name=entity.product_name,
                quantity=entity.quantity,
                total_price=int(entity.total_price),
                customer_id=entity.customer_id
            )
        return self._to_entity(obj)

    def get_by_id(self, order_id: int) -> Optional[OrderEntity]:
        try:
            obj = Order.objects.get(id=order_id)
            return self._to_entity(obj)
        except Order.DoesNotExist:
            return None

    def delete(self, order_id: int) -> None:
        Order.objects.filter(id=order_id).delete()

    def list_all(self, filters: dict) -> List[OrderEntity]:
        query_filters = {}
        if 'customer_id' in filters:
            query_filters['customer_id'] = filters['customer_id']
        if 'min_price' in filters:
            query_filters['total_price__gte'] = filters['min_price']
        if 'max_price' in filters:
            query_filters['total_price__lte'] = filters['max_price']
        if 'start_date' in filters:
            query_filters['created_at__date__gte'] = filters['start_date']
        if 'end_date' in filters:
            query_filters['created_at__date__lte'] = filters['end_date']

        qs = Order.objects.filter(**query_filters).order_by('-created_at')
        return [self._to_entity(obj) for obj in qs]
