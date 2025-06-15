from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "Главная страница сервиса рассылок. Перейдите в /admin/ или /mailings/."
    )


urlpatterns = [
    path("", home),  # Добавь эту строчку ПЕРВОЙ!
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("mailings/", include("mailings.urls")),
]
