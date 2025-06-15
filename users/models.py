from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = "user"
    MANAGER = "manager"
    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (MANAGER, "Менеджер"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    is_blocked = models.BooleanField(default=False)

    def is_manager(self):
        return self.role == self.MANAGER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
