from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .forms import PrivateMessageForm, ConversationMessageForm
from django.contrib import messages
from django.conf import settings
from .models import PrivateMessage, Conversation
from ads.models import Ad
from django.contrib.auth.models import User
from django.db.models import Q
<< << << < HEAD
== == == =
>>>>>> > dc54500bfd7d097a06bc1acf1c5424f88895ec5c


# Create your views here.

# list messages in inbox
def inbox(request):
    conversations = Conversation.objects.filter(
        Q(starter=request.user) | Q(participant=request.user))
    context = {'conversations': conversations}
    return render(request, 'private_messages/inbox.html', context)

# list messages in specific conversation


def conversation(request, pk):
    form = ConversationMessageForm()
    conversation = Conversation.objects.get(pk=pk)
    private_messages = PrivateMessage.objects.filter(conversation=conversation)
    context = {'private_messages': private_messages,
               'conversation': conversation, 'form': form}
    return render(request, 'private_messages/conversation.html', context)


# return json of messages that belongs to conversation
def conversation_json(request, pk):
    form = ConversationMessageForm()
    conversation = Conversation.objects.get(pk=pk)
    private_messages = PrivateMessage.objects.filter(conversation=conversation)

    private_messages_list = []
    for private_message in private_messages:
        private_message_data = {
            'id': private_message.id,
            'body': private_message.body,
            'date': private_message.date,
            'sender': private_message.sender.username,
        }
        private_messages_list.append(private_message_data)

    return JsonResponse(private_messages_list, safe=False)


def conversation_html(request, pk):
    conversation = Conversation.objects.get(pk=pk)
    private_messages = PrivateMessage.objects.filter(conversation=conversation)
    context = {'private_messages': private_messages,
               'conversation': conversation}
    return render(request, 'private_messages/conversation_html.html', context)


# start conversation when first time reply to an ad
def conversation_start(request):
    if request.user.is_authenticated:
        ad_id = request.GET['ad']
        ad = Ad.objects.get(id=ad_id)
        if request.method == 'POST':
            form = PrivateMessageForm(request.POST)
            if form.is_valid():
                conversation = Conversation.objects.create(
                    ad=ad, starter=request.user, participant=ad.author)
                f = form.save(commit=False)
                f.sender = request.user
                f.conversation = conversation
                f.save()

                # >> send notification email
                subject = "New Conversation"
                message = render_to_string('private_messages/new_conversation_email.html', {
                    'author': ad.author,
                    'user': request.user,
                    'ad': ad,
                    'conversation': conversation,
                    'domain': get_current_site(request).domain,
                })
                recepient_email = ad.author.email
                send_mail(subject, message, from_email=None,
                          recipient_list=[recepient_email], html_message=message)

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
                conversation = Conversation.objects.get(
                    id=request.GET['conversation'])
                f = form.save(commit=False)
                f.sender = request.user
                f.conversation = conversation
                f.save()
                return redirect(request.META['HTTP_REFERER'])
        else:
            form = PrivateMessageForm()
            return render(request, 'private_messages/send.html', {'form': form})
    else:
        messages.info(request, f'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path} ')


# form to send private message
def send_ajax(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PrivateMessageForm(request.POST)
            if form.is_valid():
                conversation = Conversation.objects.get(
                    id=request.GET['conversation'])
                f = form.save(commit=False)
                f.sender = request.user
                f.conversation = conversation
                f.save()
                return HttpResponse('success')
        else:
            return HttpResponse('not right')
    else:
        return HttpResponse('not allowed')

# list of sent messages from user
# def sent(request):
#     private_messages = PrivateMessage.objects.filter(sender=request.user)
#     context = { 'private_messages':private_messages }
#     return render(request, 'sent.html', context)
