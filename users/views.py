from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

# email activation
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from .forms import RegisterForm
from .tokens import account_activation_token


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


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, f"Thank you {user.username}, you are now logged in!.")
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid')


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
