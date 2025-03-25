from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from users.forms import RegisterForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def no_permission(request):
    return render(request, 'users/no_permission.html')


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


@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'users/admin_dashboard.html', context)


@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, id):
    user = User.objects.get(id=id)
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

    context = {
        'form': form,
        'user': user,
    }

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

    context = {
        'form': form,
    }

    return render(request, 'users/create_group.html', context)


@user_passes_test(is_admin, login_url='no_permission')
def group_list(request):
    groups = Group.objects.all()
    context = {
        'groups': groups,
    }
    return render(request, 'users/group_list.html', context)
