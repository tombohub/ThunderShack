from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ad
from .forms import AdCreateForm
from django.contrib import messages
from django.conf import settings

# Create your views here.
def home(request):
    context = {
        'ads': Ad.objects.all()
    }
    return render(request, 'ads/home.html', context)

def create_ad(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AdCreateForm(request.POST)
            if form.is_valid():
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



