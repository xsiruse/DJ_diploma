from django.shortcuts import render
from django.views import generic

from .forms import UserCreateForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate

from app.models import Product, Category, Cart, CartItem, Order, Review, Article
from app.forms import OrderForm, ReviewForm
from django.contrib.auth.models import User


def account_view(request):
    context = {}
    try:
        context['orders'] = Order.objects.filter(user=request.user).order_by('-pk')
    except:
        context['orders'] = None
    return render(request, 'app/account.html', context)


class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def main_view(request):
    context = {}
    context['phones'] = Product.objects.filter(category__title='phones')
    context['articles'] = Article.objects.all().order_by('-date')[:5]
    context['other'] = Product.objects.filter(category__title='other')
    return render(request, 'app/index.html', context)


def article_view(request, *args, **kwargs):
    context = {}
    slug = kwargs['slug']
    context['article'] = get_object_or_404(Article, slug=slug)
    return render(request, 'app/article.html', context)


# Product views
def product_detail_view(request, *args, **kwargs):
    context = {}
    slug = kwargs['slug']
    product = get_object_or_404(Product, slug=slug)
    context['product'] = product

    form = ReviewForm(request.POST or None)
    context['form'] = form

    if form.is_valid():
        new_review = Review()
        new_review.user = request.user
        new_review.rating = int(form.cleaned_data['rating'])
        new_review.save()
        new_review.product.add(product)
        new_review.save()
        new_review.text = form.cleaned_data['text']
        new_review.save()

    context['reviews'] = Product.objects.get(slug=slug)
    return render(request, 'app/product_detail.html', context)


def products_of_category_view(request, *args, **kwargs):
    slug = kwargs['slug']
    context = {}
    context['products'] = Product.objects.filter(category__title__iexact=slug)
    return render(request, 'app/products_of_category.html', context)


def accessories_of_category_view(request, *args, **kwargs):
    slug = kwargs['slug']
    context = {}
    context['products'] = Product.objects.filter(category__title__iexact=slug)
    return render(request, 'app/products_of_category.html', context)


# Cart views

def cart_session(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def cart_view(request):
    context = {}
    context['cart'] = cart_session(request)
    return render(request, 'app/cart.html', context)


def add_to_cart_view(request):
    slug = request.GET.get('slug')
    cart = cart_session(request)
    product = Product.objects.get(slug=slug)
    cart.add_to_cart(product)

    cart.count_cart_total()
    return JsonResponse({})


def remove_from_cart_view(request):
    slug = request.GET.get('slug')
    cart = cart_session(request)
    product = Product.objects.get(slug=slug)
    cart.remove_from_cart(product)

    cart_total = cart.count_cart_total()
    return JsonResponse({'cart_total': cart_total})


def change_item_quantity_view(request):
    context = {}
    cart = cart_session(request)
    context['cart'] = cart
    quantity = int(request.GET.get('quantity', 1))
    item_id = int(request.GET.get('item_id', 1))

    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.change_quantity(quantity)

    cart_total = cart.count_cart_total()

    return JsonResponse({'item_total': cart_item.item_total,
                         'cart_total': cart_total})


def checkout_view(request):
    context = {}
    context['cart'] = cart_session(request)
    return render(request, 'app/checkout.html', context)


def order_create_view(request):
    context = {}
    form = OrderForm(request.POST or None)
    context['form'] = OrderForm(request.POST or None)
    cart = cart_session(request)
    context['cart'] = cart

    if form.is_valid():
        new_order = Order()
        new_order.user = request.user
        new_order.cart = cart
        new_order.save()
        new_order.first_name = form.cleaned_data['first_name']
        new_order.last_name = form.cleaned_data['last_name']
        new_order.phone = form.cleaned_data['phone']
        new_order.buying_type = form.cleaned_data['buying_type']
        new_order.address = form.cleaned_data['address']
        new_order.comment = form.cleaned_data['comment']
        new_order.total = cart.cart_total
        new_order.save()

        del request.session['cart_id']
        return HttpResponseRedirect(reverse('congratulations'))
    return render(request, 'app/order.html', context)


def congratulations_view(request):
    context = {}
    return render(request, 'app/congratulations.html', context)


def empty_section(request):
    context = {}
    return render(request, 'app/empty_section.html', context)
