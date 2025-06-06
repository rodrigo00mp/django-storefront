from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):

    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory_status', 'collections']
    list_per_page = 10
    list_filter = ['collections', 'last_update', InventoryFilter]
    actions = ['clear_inventory']
    inlines = [ProductImageInline]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Okay'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f'{updated_count} products were succesfully updated')

    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10
    list_select_related = ['user']

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
            products_count=Count('products')
        )
