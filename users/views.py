from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"Hi {username}, your registration is successfull! Please check the mail and confirm your account.")
            form.save()
            return redirect('login')

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
