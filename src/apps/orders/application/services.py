from apps.orders.domain.entities import OrderEntity


class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def get_orders_for_user(self, user, query_params: dict):
        filters = {}
        if not user.is_admin():
            filters['customer_id'] = user.id

        if 'min_price' in query_params:
            filters['min_price'] = query_params['min_price']
        if 'start_date' in query_params:
            filters['start_date'] = query_params['start_date']
        if 'end_date' in query_params:
            filters['end_date'] = query_params['end_date']

        return self.repository.list_all(filters)

    def create_order(self, customer_id, product_name, quantity, unit_price):
        total_price = quantity * unit_price
        order = OrderEntity(
            product_name=product_name,
            quantity=quantity,
            total_price=total_price,
            customer_id=customer_id
        )
        return self.repository.save(order)

    def update_order_securely(self, order_id, user, data):
        order = self.repository.get_by_id(order_id)
        if not order:
            return None

        if not user.is_admin() and order.customer_id != user.id:
            raise PermissionError("Access Denied")

        order.product_name = data.get('product_name', order.product_name)
        if 'quantity' in data or 'unit_price' in data:
            qty = data.get('quantity', order.quantity)
            price = data.get('unit_price', float(order.total_price) / order.quantity)
            order.total_price = qty * price
            order.quantity = qty

        return self.repository.save(order)

    def delete_order_securely(self, order_id, user):
        order = self.repository.get_by_id(order_id)
        if not order:
            return False

        if not user.is_admin() and order.customer_id != user.id:
            raise PermissionError("Access Denied")

        self.repository.delete(order_id)
        return True
