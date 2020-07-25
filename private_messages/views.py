from django.shortcuts import render, redirect
from .forms import PrivateMessageForm
from django.contrib import messages
from django.conf import settings
from .models import PrivateMessage
from django.contrib.auth.models import User


# Create your views here.

# list messages in inbox
def inbox(request):
    private_messages = PrivateMessage.objects.filter(receiver=request.user)
    context = {'private_messages':private_messages}
    return render(request, 'private_messages/inbox.html', context)


# form to send private message
def send(request):
    if request.user.is_authenticated:                
        ad_id = request.GET['ad']              
        receiver = User.objects.get(username=request.GET['to'])
        if request.method == 'POST':                       
            form = PrivateMessageForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.sender = request.user
                f.receiver = receiver
                f.ad_id = ad_id
                f.save()
                messages.success(request, f'Message sent!')
                return redirect('ads-home')
        else:
            form = PrivateMessageForm()
            return render(request, 'private_messages/send.html', {'form':form})
    else: 
        messages.info(request, f'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path} ')

# list of sent messages from user
def sent(request):
    private_messages = PrivateMessage.objects.filter(sender=request.user)
    context = { 'private_messages':private_messages }
    return render(request, 'sent.html', context)