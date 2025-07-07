from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ClientForm, MailingForm, MessageForm
from .models import Client, Mailing, MailingAttempt, Message

User = get_user_model()


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"

    def test_func(self):
        # Видно только админу или staff-пользователю
        return self.request.user.is_staff or self.request.user.is_superuser


def index(request):
    mailing_count = Mailing.objects.count()
    active_count = Mailing.objects.filter(status="started").count()
    unique_clients = Client.objects.values("email").distinct().count()
    context = {
        "mailing_count": mailing_count,
        "active_count": active_count,
        "unique_clients": unique_clients,
    }
    return render(request, "mailings/index.html", context)


# --- Клиенты ---
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailings/clients/list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "mailings/clients/detail.html"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailings/clients/form.html"
    success_url = reverse_lazy("mailings:clients_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailings/clients/form.html"
    success_url = reverse_lazy("mailings:clients_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "mailings/clients/confirm_delete.html"
    success_url = reverse_lazy("mailings:clients_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


# --- Сообщения ---
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/messages/list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailings/messages/detail.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/messages/form.html"
    success_url = reverse_lazy("mailings:messages_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/messages/form.html"
    success_url = reverse_lazy("mailings:messages_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/messages/confirm_delete.html"
    success_url = reverse_lazy("mailings:messages_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


# --- Рассылки ---
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailings/list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailings/detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailings/form.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "Создана"
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailings/form.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


@login_required
def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, user=request.user)
    attempt_status = "success"
    response = "Письмо отправлено успешно."
    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[client.email],
            )
        except Exception as e:
            attempt_status = "fail"
            response = str(e)
        MailingAttempt.objects.create(
            mailing=mailing, status=attempt_status, server_response=response
        )
    if mailing.status == "created":
        mailing.status = "started"
        mailing.save()
    return redirect("mailings:mailings_detail", pk=mailing.pk)


class MailingAttemptsListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailings/mailings/attempts_list.html"

    def get_queryset(self):
        return MailingAttempt.objects.filter(mailing_id=self.kwargs["pk"])


# --- Активация/деактивация рассылок (только для staff) ---
@user_passes_test(lambda u: u.is_staff)
def deactivate_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == "POST":
        mailing.is_active = False
        mailing.save()
    return redirect("mailings:mailings_list")


@user_passes_test(lambda u: u.is_staff)
def activate_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == "POST":
        mailing.is_active = True
        mailing.save()
    return redirect("mailings:mailings_list")
