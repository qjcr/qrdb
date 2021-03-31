from django.http import HttpResponse
from django.shortcuts import render

from . import models

def index(request):
    return render(request, "test.html")

def view_map(request):
    feed_dict = {}
    feed_dict['buildings'] = models.Building.objects.all()
    return render(request, "test.html", feed_dict)

