from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Allows access only to authenticated users with ADMIN role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsCustomerUser(permissions.BasePermission):
    """Allows access only to authenticated users with CUSTOMER role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CUSTOMER'


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allows access to administrators or the resource owner."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        return obj.customer_id == request.user.id
