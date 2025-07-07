from django import forms

from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "status", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "clients": forms.SelectMultiple(),
        }
        labels = {
            "start_time": "Дата и время первой отправки",
            "end_time": "Дата и время окончания отправки",
            "status": "Статус рассылки",
            "message": "Выберите сообщение",
            "clients": "Получатели рассылки",
        }
        help_texts = {
            "start_time": "Укажите дату и время, когда рассылка начнётся.",
            "end_time": "Укажите дату и время окончания рассылки.",
            "status": "Выберите статус для рассылки (Создана, Запущена, Завершена).",
            "message": "Выберите ранее созданное сообщение, которое будет отправлено.",
            "clients": "Выберите одного или нескольких получателей.",
        }
