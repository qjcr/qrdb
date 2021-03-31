from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import models

def index(request):
    return render(request, "test.html")

@login_required
def view_map(request):
    print(request.user)
    feed_dict = {}
    feed_dict['buildings'] = models.Building.objects.all()
    return render(request, "test.html", feed_dict)

@login_required
def view_staircase(request, staircase_name):
    feed_dict = {}

    print(staircase_name)
    staircase = models.Staircase.objects.get(name=staircase_name)

    feed_dict['staircase'] = staircase
    feed_dict['rooms'] = staircase.room_set.all() 
    return render(request, "staircase.html", feed_dict)