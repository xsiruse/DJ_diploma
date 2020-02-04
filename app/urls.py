
from django.urls import path
from app.views import (main_view,
                       cart_view,
                       empty_section,
                       products_of_category_view,
                       product_detail_view,
                       add_to_cart_view,
                       remove_from_cart_view,
                       change_item_quantity_view,
                       checkout_view,
                       order_create_view,
                       congratulations_view,
                       article_view, accessories_of_category_view)

urlpatterns = [
    path('', main_view, name='main_page'),
    path('category/<str:slug>/', products_of_category_view, name='category'),
    path('product/<str:slug>/', product_detail_view, name='product'),
    path('accessories/<str:slug>/', accessories_of_category_view, name='accessories'),
    path('articles/<str:slug>/', article_view, name='article'),
    path('cart/', cart_view, name='cart'),
    path('cart/remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/change_item_quantity/', change_item_quantity_view, name='change_item_quantity'),
    path('cart/add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),
    path('cart/order/', order_create_view, name='order_create'),
    path('cart/congratulations/', congratulations_view, name='congratulations'),
    path('empty_section/', empty_section, name='empty_section'),
]