from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from django.conf import settings

from decimal import Decimal

from transliterate import translit


def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            instance.slug = slugify(translit(instance.title, reversed=True))
        except:
            instance.slug = slugify(instance.title)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


pre_save.connect(pre_save_slug, sender=Category)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField()
    description = models.TextField()
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Гаджет'
        verbose_name_plural = 'Гаджеты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})


pre_save.connect(pre_save_slug, sender=Product)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    product = models.ManyToManyField('Product', related_name='reviews')

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return f'Review №{self.pk}'


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(Product, related_name='article')
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})


pre_save.connect(pre_save_slug, sender=Article)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Корзина с {self.product.title}'

    def change_quantity(self, quantity):
        cart_item = self
        cart_item.quantity = quantity
        cart_item.item_total = Decimal(cart_item.product.price) * quantity
        cart_item.save()


class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.pk}'

    def add_to_cart(self, product):
        cart = self
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product):
        cart = self
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def count_cart_total(self):
        cart = self
        new_cart_total = Decimal(0.00)
        for item in cart.items.all():
            new_cart_total += Decimal(item.item_total)

        cart.cart_total = new_cart_total
        cart.save()
        return cart.cart_total


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')),
                                   default='Самовывоз')
    address = models.CharField(max_length=500, default='Самовывоз', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Принят в обработку')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk}'
