"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy, include, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from app.views import SignUp, account_view, main_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_page'),
    path('', include('django.contrib.auth.urls')),
    path('shop/', include('app.urls')),
    path('account/', account_view, name='account'),
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/registration/', SignUp.as_view(), name='registration'),
    path('account/logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('main_page')), name='logout'),
    re_path(r'^accounts/+', RedirectView.as_view(url=reverse_lazy('account'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
