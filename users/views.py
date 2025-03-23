from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"Hi {username}, your registration is successfull! Please check the mail and confirm your account.")
            return redirect('login')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('events:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("login")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User doesn't exist")
