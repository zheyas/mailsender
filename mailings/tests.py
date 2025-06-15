from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client, Message, Mailing


class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="1234")

    def test_create_client(self):
        client = Client.objects.create(
            email="test@example.com", full_name="Test User", user=self.user
        )
        self.assertEqual(client.email, "test@example.com")


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="1234")

    def test_create_message(self):
        message = Message.objects.create(subject="Subject", body="Body", user=self.user)
        self.assertEqual(message.subject, "Subject")
