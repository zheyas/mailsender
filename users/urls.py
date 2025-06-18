from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path(
        "logout/", auth_views.LogoutView.as_view(next_page="login"),
        name="logout"
    ),

    path("profile/", views.profile, name="profile"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view
        (template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("signup/", views.register, name="signup"),   # лишний, если не нужен
    path('list/', views.user_list, name='user_list'),
    path('<int:pk>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('<int:pk>/activate/', views.activate_user, name='activate_user'),
]
