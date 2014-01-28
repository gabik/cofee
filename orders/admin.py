from django.contrib import admin
from orders.models import client_orders, item_size, item_strong, order_cart, item_status

admin.site.register(client_orders)
admin.site.register(item_size)
admin.site.register(item_strong)
admin.site.register(item_status)
admin.site.register(order_cart)

