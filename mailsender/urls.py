from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return redirect('/mailings/')


urlpatterns = [
    path("", home),  # Первая! Главное, чтобы она была первой.
    path("admin/", admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path("users/", include("users.urls")),  # Для своей регистрации/профиля
    path("mailings/", include("mailings.urls")),
]