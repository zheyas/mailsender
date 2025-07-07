from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Client, Message

User = get_user_model()


class ClientModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_create_client(self):
        client = Client.objects.create(
            email="test@example.com", full_name="Test User", user=self.user
        )
        self.assertEqual(client.email, "test@example.com")


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="yourpassword"
        )

    def test_create_message(self):
        message = Message.objects.create(subject="Subject", body="Body", user=self.user)
        self.assertEqual(message.subject, "Subject")
