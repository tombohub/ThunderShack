from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # prepare activation email
            current_site = get_current_site(request)
            email_subject = "Please activate your account"
            email_message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),

            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, email_message, to=[to_email])
            email.send()
            username = form.cleaned_data.get('username')

            # registration complete
            messages.success(
                request, f'Thank you {username}, please check your email to complete registration')
            return redirect('/')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                messages.success(
                    request, f'Welcome back {username}! Now you can post your ad.')
                return redirect(request.GET['next'])
            else:
                messages.success(request, f'Hello {username}, welcome back!')
                return redirect('/')
        else:
            messages.error(
                request, f'Oh no! Either username "{username}" doesn\'t exist or passwords is not correct. Did you forget your password?')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    username = request.user.username
    logout(request)
    messages.success(
        request, f'Thank you {username}, you are now logged out. Have a nice day!')
    return redirect('/')


def profile(request):
    return render(request, 'users/profile.html')
