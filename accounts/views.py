from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from accounts.forms import RegisterForm, LoginForm, ProfileEditForm
from django.contrib.auth.models import User
from a2.decorators import login_required
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            User.objects.create_user(username=username, email=email,
                                     password=password, first_name=first_name, last_name=last_name)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/accounts/profile/view/')
            else:
                return render(request, "accounts/login.html", {"form": form, "error_message": "Username or password is invalid"})
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('login')


@login_required
def view_profile(request):
    user = request.user
    res = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    return JsonResponse(res)


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['first_name']:
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name']:
                user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']

            if form.cleaned_data['password1']:
                password = form.cleaned_data['password1']
                user.set_password(password)

            user.save()
            update_session_auth_hash(request, user)
            return redirect('view_profile')
    else:
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = ProfileEditForm(user_data)

    return render(request, 'accounts/edit_profile.html', {'form': form})
