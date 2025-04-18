from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory_status', 'collections']
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Okay'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode(
            {
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{}</a>', url,
                           customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode(
            {
                'collections__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url,
                           collection.products_count)

    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
