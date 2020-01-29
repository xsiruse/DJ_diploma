from django.contrib.admin import register, ModelAdmin

from .models import Product, Review, Article, Order, Category, CartItem, Cart


@register(Product)
class ProductAdmin(ModelAdmin):
    pass


@register(Review)
class ReviewAdmin(ModelAdmin):
    pass


@register(Article)
class ArticleAdmin(ModelAdmin):
    pass


def make_order_payed(modelAdmin, request, queryset):
    queryset.update(status='Оплачен')


make_order_payed.short_description = 'Пометить как оплаченные'


@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('__str__', 'user', 'status')
    list_filter = ['create_date']
    actions = [make_order_payed]


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@register(CartItem)
class CartItemAdmin(ModelAdmin):
    pass


@register(Cart)
class CartAdmin(ModelAdmin):
    pass
