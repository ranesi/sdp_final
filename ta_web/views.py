from django.shortcuts import render


def homepage(request):

    return render(request, 'ta_web/home.html')


def about(request):

    return render(request, 'ta_web/about.html')
