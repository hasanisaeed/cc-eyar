from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.orders.application.services import OrderService
from apps.orders.infrastructure.repositories.django_repo import DjangoOrderRepository
from apps.users.permissions.rbac import IsOwnerOrAdmin
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = OrderService(repository=DjangoOrderRepository())

    @extend_schema(
        parameters=[
            OpenApiParameter("min_price", type=float),
            OpenApiParameter("start_date", type=str, description="YYYY-MM-DD"),
            OpenApiParameter("end_date", type=str, description="YYYY-MM-DD"),
        ],
        responses=OrderSerializer(many=True)
    )
    def list(self, request):
        orders = self.service.get_orders_for_user(request.user, request.query_params)
        return Response(OrderSerializer(orders, many=True).data)

    @extend_schema(request=OrderSerializer, responses=OrderSerializer)
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user or not request.user.id:
            return Response({"error": "User not identified"}, status=401)

        order = self.service.create_order(
            customer_id=request.user.id,
            **serializer.validated_data
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        try:
            order = self.service.update_order_securely(pk, request.user, request.data)
            if not order:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(OrderSerializer(order).data)
        except PermissionError:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        try:
            success = self.service.delete_order_securely(pk, request.user)
            if not success:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response(status=status.HTTP_403_FORBIDDEN)
