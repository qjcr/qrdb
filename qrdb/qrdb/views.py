from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "test.html")

def view_map(request):
    return render(request, "test.html")
