from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import PrivateMessageForm
from django.contrib import messages
from django.conf import settings
from .models import PrivateMessage, Conversation
from ads.models import Ad
from django.contrib.auth.models import User


# Create your views here.

# list messages in inbox
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    context = {'conversations':conversations}
    return render(request, 'private_messages/inbox.html', context)

# list messages in specific conversation
def conversation(request, pk):
    form = PrivateMessageForm()
    conversation = Conversation.objects.get(pk=pk)
    private_messages = PrivateMessage.objects.filter(conversation=conversation)
    context = {'private_messages':private_messages, 'conversation':conversation, 'form':form}
    return render(request, 'private_messages/conversation.html', context)

def conversation_start(request):
    if request.user.is_authenticated:
        ad_id = request.GET['ad']
        ad = Ad.objects.get(id=ad_id)
        if request.method == 'POST':
            form = PrivateMessageForm(request.POST)
            if form.is_valid():
                conversation = Conversation.objects.create(ad=ad, starter=request.user)
                conversation.participants.add(request.user, ad.author)
                f = form.save(commit=False)
                f.sender = request.user
                f.receiver = ad.author
                f.conversation = conversation
                f.save()
                messages.success(request, f'Message sent!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('ads-home')
    else:
        messages.info(request, f'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')


# form to send private message
def send(request):
    if request.user.is_authenticated:                
        if request.method == 'POST':                       
            form = PrivateMessageForm(request.POST)
            if form.is_valid():
                conversation = Conversation.objects.get(id=request.GET['conversation'])  
                f = form.save(commit=False)
                f.sender = request.user
                f.conversation = conversation
                f.save()
                messages.success(request, f'Message sent!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            form = PrivateMessageForm()
            return render(request, 'private_messages/send.html', {'form':form})
    else: 
        messages.info(request, f'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path} ')

# list of sent messages from user
# def sent(request):
#     private_messages = PrivateMessage.objects.filter(sender=request.user)
#     context = { 'private_messages':private_messages }
#     return render(request, 'sent.html', context)