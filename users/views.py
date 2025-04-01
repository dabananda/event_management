from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from users.forms import RegisterForm, LoginForm, AssignRoleForm, CreateGroupForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def no_permission(request):
    return render(request, 'users/no_permission.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"Hi {username}, your registration is successful! Please check your email and confirm your account.")
            return redirect('login')
    else:
        form = RegisterForm()
    context = {'form': form}
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
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def activate_user(request, user_id, token):
    try:
        user = CustomUser.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("login")
        else:
            return HttpResponse("Invalid id or token")
    except CustomUser.DoesNotExist:
        return HttpResponse("User doesn't exist")


@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'users/admin_dashboard.html', context)


@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, id):
    user = CustomUser.objects.get(id=id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request, f"{user.username} has been assigned to {role.name} role successfully!")
            return redirect('admin_dashboard')
    context = {'form': form, 'user': user}
    return render(request, 'users/assign_role.html', context)


@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            permissions = form.cleaned_data.get('permission')
            group.permissions.set(permissions)
            messages.success(
                request, f"{group.name} has been created successfully!")
            return redirect('create_group')
    context = {'form': form}
    return render(request, 'users/create_group.html', context)


@user_passes_test(is_admin, login_url='no_permission')
def group_list(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'users/group_list.html', context)


@login_required
def profile(request):
    context = {'profile': request.user}
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone_number = form.cleaned_data.get('phone_number')
            if form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data.get('profile_picture')
            user.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        })
    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)
