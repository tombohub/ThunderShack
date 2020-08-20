from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from decouple import config


def posting_policy(request):
    return render(request, 'posting_policy.html')


def terms_of_use(request):
    return render(request, 'terms_of_use.html')


def cookie_policy(request):
    return render(request, 'cookie_policy.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # SEND EMAIL
            subject = form.cleaned_data.get('subject')
            name = form.cleaned_data.get('name')
            sender_email = form.cleaned_data.get('email')
            recepient_email = config('CONTACT_US_EMAIL')
            email_message = f"{form.cleaned_data.get('message')}\n\n{name}"
            send_mail(subject, email_message, sender_email,
                      [recepient_email])

            messages.success(
                request, f'Message sent! Thank you for contacting')
            return redirect('/')
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})
