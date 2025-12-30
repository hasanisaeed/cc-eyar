from django.contrib import admin
from apps.orders.infrastructure.models.order import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'customer_link', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at', 'customer', 'total_price')
    search_fields = ('product_name', 'customer__username', 'customer__email')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    list_per_page = 20

    def customer_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse

        url = reverse('admin:users_user_change', args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>', url, obj.customer.username)

    customer_link.short_description = 'Customer'
