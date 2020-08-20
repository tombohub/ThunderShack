from django.shortcuts import render


def posting_policy(request):
    return render(request, 'posting_policy.html')
