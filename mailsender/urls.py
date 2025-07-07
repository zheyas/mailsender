from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home(request):
    return redirect("/mailings/")


urlpatterns = [
    path("", home),  # Первая! Главное, чтобы она была первой.
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),  # Для своей регистрации/профиля
    path("mailings/", include("mailings.urls")),
]
