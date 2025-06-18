from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, Message, MailingAttempt
from .forms import ClientForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import MailingForm
from django.shortcuts import get_object_or_404, redirect
from .models import Mailing
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView


class UserListView(ListView):
    model = get_user_model()
    template_name = 'mailings/user_list.html'

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
    template_name = 'mailings/mailings/messages_create.html'
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
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

def mailing_create(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailings:messages_list')
    else:
        form = MailingForm()
    return render(request, "mailings/mailings/form.html", {
        "form": form,
        "title": "Создать рассылку"
    })

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

@user_passes_test(lambda u: u.is_staff)
def deactivate_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.is_active = False
    mailing.save()
    return redirect('mailings:mailings_list')

@user_passes_test(lambda u: u.is_staff)
def activate_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.is_active = True
    mailing.save()
    return redirect('mailings:mailings_list')

@user_passes_test(lambda u: u.is_staff)
def deactivate_user(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    user.is_active = False
    user.save()
    return redirect('mailings:users_list')

@user_passes_test(lambda u: u.is_staff)
def activate_user(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    user.is_active = True
    user.save()
    return redirect('mailings:users_list')