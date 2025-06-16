
# mailings/urls.py
from django.urls import path
from . import views

app_name = "mailings"

urlpatterns = [
    # Главная страница
    path("", views.index, name="index"),

    # Клиенты
    path("clients/", views.ClientListView.as_view(), name="clients_list"),
    path("clients/create/", views.ClientCreateView.as_view(),
         name="clients_create"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(),
         name="clients_detail"),
    path("clients/<int:pk>/update/", views.ClientUpdateView.as_view(),
         name="clients_update"),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(),
         name="clients_delete"),

    # Сообщения
    path("messages/", views.MessageListView.as_view(), name="messages_list"),
    path("messages/create/", views.MessageCreateView.as_view(),
         name="messages_create"),
    path("messages/<int:pk>/", views.MessageDetailView.as_view(),
         name="messages_detail"),
    path("messages/<int:pk>/update/", views.MessageUpdateView.as_view(),
         name="messages_update"),
    path("messages/<int:pk>/delete/", views.MessageDeleteView.as_view(),
         name="messages_delete"),

    # Рассылки
    path("mailings/", views.MailingListView.as_view(), name="mailings_list"),
    path("mailings/create/", views.MailingCreateView.as_view(),
         name="mailings_create"),
    path("mailings/<int:pk>/", views.MailingDetailView.as_view(),
         name="mailings_detail"),
    path("mailings/<int:pk>/update/", views.MailingUpdateView.as_view(),
         name="mailings_update"),
    path("mailings/<int:pk>/delete/", views.MailingDeleteView.as_view(),
         name="mailings_delete"),
    path("mailings/<int:pk>/send/", views.send_mailing, name="mailings_send"),
    path("mailings/<int:pk>/attempts/",
         views.MailingAttemptsListView.as_view(),
         name="mailing_attempts"),
]
