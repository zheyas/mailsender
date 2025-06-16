from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('/mailings/')  # Главная страница - редирект на mailings

urlpatterns = [
    path("", home),  # Первая! Главное, чтобы она была первой.
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # Для login/logout/password
    path("users/", include("users.urls")),  # Для своей регистрации/профиля
    path("mailings/", include("mailings.urls")),
]
