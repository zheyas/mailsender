from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти.")
            return redirect('users:login')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("users:profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "users/profile.html")


@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})


@user_passes_test(lambda u: u.is_staff)
def deactivate_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f"Пользователь {user.username} заблокирован.")
    return redirect('users:user_list')


@user_passes_test(lambda u: u.is_staff)
def activate_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        messages.success(request, f"Пользователь {user.username} активирован.")
    return redirect('users:user_list')
