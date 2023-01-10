from django.contrib import admin

# Register your models here.

from webapp.models import Item, ItemsOrders, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'balance', 'price']
    list_display_links = ['name']
    list_filter = ['category']
    fields = ['name', 'description', 'category', 'balance', 'price']


admin.site.register(Item, ItemAdmin)


# class BasketAdmin(admin.ModelAdmin):
#     list_display = ['id', 'item', 'amount']
#     list_display_links = ['item']
#     list_filter = ['item']
#     fields = ['item', 'amount']
#
#
# admin.site.register(Basket, BasketAdmin)


class ItemsOrdersInLine(admin.TabularInline):
    model = ItemsOrders


class ItemsOrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'order', 'quantity']
    list_display_links = ['item']
    list_filter = ['item']
    fields = ['item', 'order', 'quantity']


admin.site.register(ItemsOrders, ItemsOrdersAdmin)


class OrderAdmin(admin.ModelAdmin):

    inlines = [
        ItemsOrdersInLine
    ]
    list_display = ['id', 'username', 'phonenumber', "created_at"]
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    fields = ['username', 'phonenumber', 'address', "created_at"]


admin.site.register(Order, OrderAdmin)