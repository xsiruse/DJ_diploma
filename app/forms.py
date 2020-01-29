from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Review


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': _("Логин"),
            'password1': _("Пароль"),
            'password2': _('Проверка пароля'),
        }


class OrderForm(forms.ModelForm):
    class Meta(object):
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'comment'
        )

        labels = {
            'first_name': 'Ваше имя:',
            'last_name': 'Ваша фамилия:',
            'phone': 'Номер телефона:',
            'address': 'Адресс доставки:',
            'buying_type': 'Тип доставки:',
            'comment': 'Комментарий:',
        }

        help_texts = {
            'phone': 'Пожалуйста, укажите реальный номер телефона, по которому с Вами можно связаться',
            'address': '*Обязательно укажите адресс!'
        }


RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'rating'}), choices=RATING_CHOICES)
    rating.label = 'Оцените:'


    class Meta(object):
        model = Review
        fields = (
            'text',
            'rating',
        )

        labels = {
            'text': 'Комментарий:',
        }

