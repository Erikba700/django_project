from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import LoginForm, RegisterForm


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.profile.phone_number = form.cleaned_data["phone_number"]
            instance.profile.country = form.cleaned_data["country"]
            instance.profile.save()
            messages.success(request, "The Profile created successfully")
            return redirect("pizza:list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, "user/registration.html",
                  {"form": form})


def login_user(request):
    form = LoginForm()
    next_url = request.GET.get("next")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username=form.cleaned_data["username"])
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect("pizza:list")
    return render(request, "user/login.html", {"form": form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("pizza:list")
