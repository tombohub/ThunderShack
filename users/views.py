from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created, {username}')
            return redirect('/')
    else:
        form = RegisterForm()
    context = { 'form': form }
    return render(request, 'users/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if  'next' in request.GET:
                messages.success(request, f'Welcome back {username}! Now you can post your ad.')
                return redirect(request.GET['next'])
            else:
                messages.success(request, f'Hello {username}, welcome back!')
                return redirect('/')
        else:
            messages.error(request, f'Oh no! Either username "{username}" doesn\'t exist or passwords is not correct. Did you forget your password?')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    username = request.user.username
    logout(request)
    messages.success(request, f'Thank you {username}, you are now logged out. Have a nice day!')
    return redirect('/')
