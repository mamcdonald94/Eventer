from django.http.response import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('test')

def event_info(request):
    return render(request, 'event_info.html')
