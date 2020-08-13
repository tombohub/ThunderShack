from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ad
from django.contrib.auth.models import User
from .forms import AdCreateForm
from private_messages.forms import PrivateMessageForm
from private_messages.models import Conversation
from django.contrib import messages
from django.conf import settings


# Home page. List ads.
def home(request):
    context = {
        'ads': Ad.objects.all()
    }
    return render(request, 'ads/home.html', context)


# create new ad form
def create_ad(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AdCreateForm(request.POST, request.FILES)
            if form.is_valid():
                # commit false so we add user after
                f = form.save(commit=False)
                f.author = request.user
                f.save()
                title = form.cleaned_data.get('title')
                messages.success(request, f'Your ad "{title}" is now posted!')
                return redirect('ads-home')
        else:
            form = AdCreateForm()
            return render(request, 'ads/create_ad.html', {'form': form})
    else:
        messages.info(request, 'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')

# delete ad by its author


def delete(request, pk):
    if request.user.is_authenticated:
        ad = Ad.objects.get(pk=pk)
        if ad.author == request.user:
            ad.delete()
            messages.info(request, f'ad {ad.title} deleted!')
            return redirect('user-ads')
    else:
        messages.info(request, 'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')


# edit the single ad
def edit(request, pk):
    if request.user.is_authenticated:  # 1
        ad = Ad.objects.get(pk=pk)
        if ad.author == request.user:  # 2
            if request.method == 'POST':  # 3
                form = AdCreateForm(request.POST, request.FILES, instance=ad)
                if form.is_valid():  # 4
                    # commit false so we add user after
                    f = form.save(commit=False)
                    f.author = request.user
                    f.save()
                    title = form.cleaned_data.get('title')
                    messages.success(
                        request, f'Your ad "{title}" is now updated!')
                    return redirect('user-ads')
            else:  # 3
                form = AdCreateForm(instance=ad)
                return render(request, 'ads/edit.html', {'form': form})
    else:  # 1
        messages.info(request, 'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')

# single ad view


def ad_details(request, pk, slug):
    ad = Ad.objects.get(slug=slug, pk=pk)
    if request.user.is_authenticated:
        conversation = Conversation.get_if_exists(ad=ad, starter=request.user)
    else:
        conversation = None
    form = PrivateMessageForm()
    context = {'ad': ad, 'form': form, 'conversation': conversation}
    return render(request, 'ads/ad_details.html', context)

# list current user ads


def user_ads(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(username=request.user).id
        ads = Ad.objects.filter(author=user_id)
        context = {'ads': ads}
        return render(request, 'ads/user_ads_list.html', context)
    else:
        messages.info(request, 'Please login first')
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
